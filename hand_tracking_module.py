import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands = 2, detectionCon = 1, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        #self.modelComplex = modelComplex

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks) # to detect hand

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) # membuat tracking titik sendi dan koneksi antar sendi tangan
        return img
    
    def findPosition(self, img, handNo = 0, draw = True):
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                #print(id, lm)
                height, width, channel = img.shape
                cx, cy = int(lm.x*width), int(lm.y*height)
                lmList.append([id, cx, cy])
                #print(id, cx, cy)
                if draw:
                    if (id == 4):
                        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    elif (id == 8):
                        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        return lmList

    
def main():
    pTime = 0 # previous time
    cTime = 0 # current time
    cap = cv2.VideoCapture(0)
    detector = handDetector()

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

if __name__ == "__main__":
    main()