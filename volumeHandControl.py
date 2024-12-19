import cv2
import numpy as np
import time
import mediapipe as mp
import handTrackingModule as htm
import math
import pycaw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volumeRange=volume.GetVolumeRange()
#print(volumeRange)
minVol = volumeRange[0]
maxVol = volumeRange[1]

wcam, hcam = 640,420
currTime=0
prevTime=0
detector = htm.handDetector(detectionConfi=0.7)
vol=0
volBar=400
volPer=0

cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
while True:
    success, img = cap.read()
    img = cv2.flip(img,flipCode=1)
    img = detector.find_hands(img)
    landmarkList = detector.findPosition(img)
    if len(landmarkList) !=0:
        
        x1,y1= landmarkList[4][1],landmarkList[4][2]
        x2,y2 = landmarkList[8][1], landmarkList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        #print(landmarkList)
        cv2.line(img,pt1=(x1,y1),pt2=(x2,y2),color=(255,0,80),thickness=2)
        cv2.circle(img,(cx,cy),8,(255,0,80),thickness=-1)

        length = math.hypot(x2-x1,y2-y1)
        #print(length)

        #approximate hand range: 0-300
        #volume range: -65 - 0
        vol = np.interp(length,[50,300],[minVol,maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])

        print(length,vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length<50:
            cv2.circle(img, (cx, cy), 8, (0, 0, 80), thickness=-1)

    cv2.rectangle(img,(50,100),(85,400),(0,255,150),2)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 150), -1)
    cv2.putText(img, f'Vol: {int(volPer)}%', (40,450), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

    currTime = time.time()
    fps = 1/(currTime-prevTime)
    prevTime = currTime

    cv2.putText(img,f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
    cv2.imshow("video", img)
    cv2.waitKey(1)