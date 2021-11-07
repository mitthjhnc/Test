import cv2
import numpy as np
import HandTrackingMinModule as htm
import time
import autopy

###################################
wCam, hCam = 640, 480
frameR = 100 #Frame Rduction
smoothening = 5
###################################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands = 1)
wScr, hScr = autopy.screen.size()

while True:
    # 1. find hand landmarks
    succes, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

     #  2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
   
        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam- frameR), (255, 0, 255), 2)    
        #  4. Only index finger : Moving mode
        if fingers[1] == 1 and fingers[2] == 0:

            # 5. Converr coordinates   

            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
            
            # 6. Smoothen Value
            # clocX = plocX + (x3 - plocX) / smoothening
            # clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse
            # autopy.mouse.move(wScr - clocX, clocY)
            autopy.mouse.move(wScr - x3, y3)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
    # 8. Both Index and middle fingers are up: Clicking Mode

    # 9. find distance between fingers
    # 10. Click mouse if distance short
        if fingers == [1, 1, 1, 1, 1]:
            autopy.mouse.toggle(down = True)
        elif fingers[1] == 1 and fingers[4] == 1:
            autopy.mouse.toggle(down = False)
        elif fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8,12, img)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()


    # 11. fps
    # cTime = time.time()
    # fps = 1/(cTime-pTime)
    # pTime = cTime
    # cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
