import time as time
import mediapipe as mp
import cv2
import handTrackingModule as htm
cap = cv2.VideoCapture(0)
prevTime = 0
currTime = 0
detector = htm.handDetector()
while True:
    success, img = cap.read()
    img = cv2.flip(img, flipCode=1)
    img = detector.find_hands(img,draw=False)
    landmarkList = detector.findPosition(img,draw=False)
    if len(landmarkList) !=0:
        print(landmarkList[4],"\n",landmarkList[8])
    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    cv2.imshow("video", img)
    cv2.waitKey(1)