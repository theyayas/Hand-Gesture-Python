import cv2
import mediapipe as mp
import time
import hand_tracking_module as htm # Import modulenya. ini penting 

pTime = 0 # previous time
cTime = 0 # current time
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)

    if (len(lmlist) != 0):
        print(lmlist[4], lmlist[8])
 
        # MENCARI FRAME RATE
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
        # MENAMPILKAN FRAME RATE
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3 )

        # MEMBUKA KAMERA
    cv2.imshow("Image", img)
    cv2.waitKey(1)