

from unittest import skip
import cv2
import csv
import cvzone
from cvzone.HandTrackingModule import HandDetector
import threading
import subprocess
import time

class myThread (threading.Thread):
    def __init__(self, threadID, program):
        # print("Created thread")
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.program=program
        self.path=self.program[0]
    
    def start_program(self):
        subprocess.run(('cmd', '/C', 'start', '', self.path))


discord=["C:/Users/laure/AppData\Local/Discord/app-1.0.9004/Discord.exe", "Discord.exe"]
youtube=["C:/Users/laure/Documents/GitHubPro/DesktopControllerAI/sites/YouTube.lnk", "chrome.exe"]
YOUKNOWWHO=["C:/Users/laure/Documents/GitHubPro/DesktopControllerAI/sites/LB", "chrome.exe"]
Red=["C:/Users/laure/Documents/GitHubPro/DesktopControllerAI/sites/LB", "chrome.exe"]
hugo=["C:/Users/laure/Documents/GitHubPro/DesktopControllerAI/img/hugo.png", "Microsoft.Photos.exe"]

pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
# cap.set(3, 1200)
# cap.set(4, 720)
detector = HandDetector()
time_first_click=0
class MCQ:
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None

    def update(self, cursor, bboxs):

        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)

def start_thread(program):
    time_first_click=time.time()
    ThreadStart = myThread(1,program)
    ThreadStart.start_program()
    return time_first_click


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, flipType=False)

    img, bbox = cvzone.putTextRect(img, "Which program do you want to open", [300, 50], 2, 2, offset=5, border=2)
    print(bbox)
    img, bbox1 = cvzone.putTextRect(img, "Discord", [160, 200], 2, 2, offset=5, border=2)
    img, bbox2 = cvzone.putTextRect(img, "Someone's stream", [800, 200], 2, 2, offset=5, border=2)
    img, bbox3 = cvzone.putTextRect(img, "Youtube", [160, 500], 2, 2, offset=5, border=2)
    img, bbox4 = cvzone.putTextRect(img, "A picture", [800, 500], 2, 2, offset=5, border=2)

    if hands:
        lmList = hands[0]['lmList']
        # here you have three values corresponding to the x, y and z  
        # The required values(location are x, and y) so we are getting those location(values) here.       
        cursor = lmList[8][:2]
        
        # print(type(cursor[0]))
        
        print(cursor)
        # 
        point1 =tuple(lmList[8][:2] )
        # print(type(point1))
        point2 =tuple(lmList[12][:2]) 
        
        # The findDistance function returns there values, 1 length, 2. info, 3. image(mat)
        length, info, img = detector.findDistance(point1, point2, img)
        length1, info, img = detector.findDistance(point1, point2, img)
        length2, info, img = detector.findDistance(tuple(lmList[0][:2]), point2, img)

            # if time.time()-time_first_click<10:
            #     print("Already opened a program in the last 10 seconds")

        if cursor[0]>150 and cursor[0]<300 and cursor[1]>170 and cursor[1]<220:
            # print("clicked on discord")
            if time_first_click:
                if time.time()-time_first_click<3:
                    # print("Already opened a program in the last 10 seconds")
                    continue
                else:
                    time_first_click=start_thread(discord)
            else:
                time_first_click=start_thread(discord)
        if cursor[0]>150 and cursor[0]<310 and cursor[1]>470 and cursor[1]<520:
            # print("clicked on youtube")
            if time_first_click:
                if time.time()-time_first_click<3:
                    # print("Already opened a program in the last 10 seconds")
                    continue
                else:
                    time_first_click=start_thread(youtube)
            else:
                time_first_click=start_thread(youtube)
        if cursor[0]>790 and cursor[0]<1120 and cursor[1]>170 and cursor[1]<220:
            # print("clicked on youknowswho")
            if time_first_click:
                if time.time()-time_first_click<3:
                    # print("Already opened a program in the last 10 seconds")
                    continue
                else:
                    time_first_click=start_thread(Red)
            else:
                time_first_click=start_thread(Red)
        if cursor[0]>790 and cursor[0]<970 and cursor[1]>470 and cursor[1]<520:
            # print("clicked on Hugo")
            if time_first_click:
                if time.time()-time_first_click<3:
                    # print("Already opened a program in the last 10 seconds")
                    continue
                else:
                    time_first_click=start_thread(hugo)
            else:
                time_first_click=start_thread(hugo)

    cv2.imshow('frame', img)
    key =cv2.waitKey(1)
    if key ==ord('q'):
        break

cv2.destroyAllWindows()