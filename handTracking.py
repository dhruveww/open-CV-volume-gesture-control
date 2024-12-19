import mediapipe as mp
import cv2
import time


cap = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands(False,2,1,0.5,0.5)
mpdraw = mp.solutions.drawing_utils

prevTime = 0
currTime = 0


while True:
    success,img = cap.read()
    img = cv2.flip(img,flipCode=1)
    imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for id,landmark in enumerate(handlandmark.landmark):
                #print(id,landmark)
                ht, wt, channel = img.shape
                cx,cy = int(landmark.x*wt), int(landmark.y*ht)
                #print(id,cx,cy)
                #if id == 4:
                #    cv2.circle(img,(cx,cy),15,(255,0,0),thickness=-1)
                #if id == 8:
                #    cv2.circle(img,(cx,cy),15,(255,0,0),thickness=-1)
    
            mpdraw.draw_landmarks(img,handlandmark,mphands.HAND_CONNECTIONS)

    currTime = time.time()
    fps = 1/(currTime-prevTime)
    prevTime=currTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),2)

    cv2.imshow("video",img)
    cv2.waitKey(1)