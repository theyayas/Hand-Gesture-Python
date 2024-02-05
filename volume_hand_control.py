import cv2
import time
import numpy as np
import hand_tracking_module as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ================== FROM PYCAW LIBRARY ========================
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()  # Min: -63.5, Max: 0.0
minVol = volRange[0]
maxVol = volRange[1]
#volume.SetMasterVolumeLevel(-20.0, None)
# ================== FROM PYCAW LIBRARY ========================

# Menentukan ukuran kamera
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
detector = htm.handDetector()

cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw = False)

    if (len(lmlist) != 0):
        #print(lmlist[4], lmlist[8])

        # mencari ujung telunjuk dan jempol
        x1, y1 = lmlist[4][1], lmlist[4][2] # ujung jempol
        x2, y2 = lmlist[8][1], lmlist[8][2] # ujung telunjuk
        cx, cy = (x1 + x2)//2, (y1 + y2)//2   # titik tengah telunjuk dan jempol

        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 1)

        # mencari jarak ujung telunjuk dan jempol
        length = math.hypot(x2 - x1, y2 - y1)
        #print(length)

        #if length < 50:
        #    cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)
        
        # hand range    : 50 - 300
        # volume range  : -63.5 - 0.0
        # CONVERT HAND RANGE TO VOLUME RANGE
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)


    # Framarate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'Framerate: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)

    cv2.imshow("Image", img)
    cv2.waitKey(1)