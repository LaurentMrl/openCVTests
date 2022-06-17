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
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.program=program
        self.path=self.program[0]
    
    def start_program(self):
        subprocess.run(('cmd', '/C', 'start', '', self.path))

discord=["C:/Users/laure/AppData\Local/Discord/app-1.0.9004/Discord.exe", "Discord.exe"]
youtube=["C:/Users/laure/Documents/GitHubPro/DesktopControllerAI/sites/YouTube.lnk", "chrome.exe"]
YOUKNOWWHO=["C:/Users/laure/Documents/GitHubPro/DesktopControllerAI/sites/YKW", "chrome.exe"]
Red=["C:/Users/laure/Documents/GitHubPro/DesktopControllerAI/sites/LB", "chrome.exe"]
hugo=["C:/Users/laure/Documents/GitHubPro/DesktopControllerAI/img/hugo.png", "Microsoft.Photos.exe"]

pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
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

def start_thread(program):
    time_first_click=time.time()
    ThreadStart = myThread(1,program)
    ThreadStart.start_program()
    return time_first_click

class Button():
    def __init__(self, program, img, button_text, button_pos, scale, thickness, offset=5, border=2):
        self.program=program
        self.button_img=img
        self.button_text=button_text
        self.button_pos=button_pos
        self.button_scale=scale
        self.button_thickness=thickness
        self.button_offset=offset
        self.button_border=border
        self.button_img,self.button_bbox=cvzone.putTextRect(self.button_img, self.button_text, self.button_pos, self.button_scale, self.button_thickness, offset=5, border=2)
    def check_if_clicked(self, cursor, time_first_click):
        if cursor[0]>self.button_bbox[0] and cursor[1]>self.button_bbox[1] and cursor[0]<self.button_bbox[2] and cursor[1]<self.button_bbox[3]:
            if time_first_click:
                if time.time()-time_first_click>3:
                    time_first_click=start_thread(self.program)                    
            else:
                time_first_click=start_thread(self.program)
        return time_first_click

while True:
    print(cap)
    success, img = cap.read()
    hands, img = detector.findHands(img, flipType=False)

    img, bbox = cvzone.putTextRect(img, "Which program do you want to open", [300, 50], 2, 2, offset=5, border=2)
    my_button_1=Button(discord, img, "Discord", [160, 200], 2, 2, offset=5, border=2)
    my_button_2=Button(YOUKNOWWHO, img, "Someone's stream", [800, 200], 2, 2, offset=5, border=2)
    my_button_3=Button(youtube, img, "Youtube", [160, 500], 2, 2, offset=5, border=2)
    my_button_4=Button(hugo, img, "A picture", [800, 500], 2, 2, offset=5, border=2)

    if hands:
        lmList = hands[0]['lmList']
        # here you have three values corresponding to the x, y and z  
        # The required values(location are x, and y) so we are getting those location(values) here.       
        cursor = lmList[8][:2]
        point1 =tuple(lmList[8][:2] )
        point2 =tuple(lmList[12][:2]) 
        
        length, info, img = detector.findDistance(point1, point2, img)
        length1, info, img = detector.findDistance(point1, point2, img)
        length2, info, img = detector.findDistance(tuple(lmList[0][:2]), point2, img)

        time_first_click=my_button_1.check_if_clicked(cursor,time_first_click)
        time_first_click=my_button_2.check_if_clicked(cursor,time_first_click)
        time_first_click=my_button_3.check_if_clicked(cursor,time_first_click)
        time_first_click=my_button_4.check_if_clicked(cursor,time_first_click)

    cv2.imshow('frame', img)
    key =cv2.waitKey(1)
    if key ==ord('q'):
        break

cv2.destroyAllWindows()