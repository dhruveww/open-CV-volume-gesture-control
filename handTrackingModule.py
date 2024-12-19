import mediapipe as mp
import cv2
import time

class handDetector():
    def __init__(self,mode=False,max_hands=2,modelComplexity=1,detectionConfi=0.7,trackConfi=0.7):
        self.mode = mode
        self.max_hands = max_hands
        self.modelComplexity = modelComplexity
        self.detectionConfi = detectionConfi
        self.trackConfi = trackConfi

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode,self.max_hands,self.modelComplexity,self.detectionConfi,self.trackConfi)
        self.mpdraw = mp.solutions.drawing_utils

    def find_hands(self,img,draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handlandmark in self.results.multi_hand_landmarks:
                #for id, landmark in enumerate(handlandmark.landmark):
                    # print(id,landmark)
                    #ht, wt, channel = img.shape
                    #cx, cy = int(landmark.x * wt), int(landmark.y * ht)
                    # print(id,cx,cy)
                    # if id == 4:
                    #    cv2.circle(img,(cx,cy),15,(255,0,0),thickness=-1)
                    # if id == 8:
                    #    cv2.circle(img,(cx,cy),15,(255,0,0),thickness=-1)
                if draw:
                    self.mpdraw.draw_landmarks(img, handlandmark, self.mphands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,handNo=0,draw=True):
        self.landmarkList = []
        if self.results.multi_hand_landmarks:
            try:
                myHand=self.results.multi_hand_landmarks[handNo]
                for id, landmark in enumerate(myHand.landmark):
                    #print(id,landmark)
                    ht, wt, channel = img.shape
                    cx, cy = int(landmark.x * wt), int(landmark.y * ht)
                    #print(id,cx,cy)
                    #if id == 4:
                    #   cv2.circle(img,(cx,cy),15,(255,0,0),thickness=-1)
                    #if id == 8:
                    #   cv2.circle(img,(cx,cy),15,(255,0,0),thickness=-1)
                    self.landmarkList.append([id,cx,cy])
                    if draw:
                        if id == 4:
                          cv2.circle(img,(cx,cy),15,(255,0,0),thickness=-1)
                        if id == 8:
                          cv2.circle(img,(cx,cy),15,(255,0,0),thickness=-1)
            except IndexError as e:
                print(f"Error: {e}. Ensure `handNo` corresponds to the correct hand.")

        return self.landmarkList

def main():
    cap = cv2.VideoCapture(0)
    prevTime = 0
    currTime = 0
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = cv2.flip(img, flipCode=1)
        img = detector.find_hands(img)
        landmarkList = detector.findPosition(img)
        if len(landmarkList) !=0:
            print(landmarkList[4],"\n",landmarkList[8])
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

        cv2.imshow("video", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()  