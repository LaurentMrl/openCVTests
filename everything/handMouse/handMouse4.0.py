from unittest import skip
import cv2
import csv
import cvzone
from cvzone.HandTrackingModule import HandDetector
import threading
import subprocess
import time
import pyautogui as PAG
from pynput.mouse import Button, Controller

class MyHand():
    def __init__(self):
        print("Init MyHand")
        self.last_hand_coor=[0,0]
        self.hand_coor=[0,0]
        self.old_left_click=None
        self.old_right_click=None
        self.new_left_click=None
        self.new_right_click=None
        self.last_left_click=time.time()
        self.new_right_click=time.time()

    def update_hand_pos(self, forefinger_tip_pos):
        self.last_hand_coor=self.hand_coor
        self.hand_coor=forefinger_tip_pos
        movement=abs((self.hand_coor[0]-self.last_hand_coor[0])+abs(self.hand_coor[1]-self.last_hand_coor[1]))
        if time.time()-self.last_left_click>=0.5:
            # if movement>=8:
            PAG.moveTo(self.hand_coor, _pause=False)
        
    def checkIfClicked(self, thumb_tip_pos, forefinger_base_pos, middle_finger_base_pos, middle_finger_tip_pos):
        if thumb_tip_pos[0]-forefinger_base_pos[0]>=-55:
            print("ça clique")
            if self.old_left_click==False:
                self.last_left_click=time.time()
                print("Left click")
                self.old_left_click=True
                mouse.press(Button.left)        
        else:
            if self.old_left_click!=False:
                self.old_left_click=False
                print("left release")
                mouse.release(Button.left)
        if middle_finger_tip_pos[1]-middle_finger_base_pos[1]>=-100:
            if self.old_right_click==False:
                self.new_right_click=time.time()
                print("Right click")
                self.old_right_click=True
                mouse.press(Button.right)
        else:
            if self.old_right_click!=False:
                self.old_right_click=False
                print("Right release")
                self.old_right_click=False
                mouse.release(Button.right)

screen_width, screen_height= PAG.size()

mouse = Controller()
detector = HandDetector()
ma_main=MyHand()

cap = cv2.VideoCapture(0)
cap.set(3, screen_width)
cap.set(4, screen_height)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, flipType=True)
    if hands:
        try:
            thumb_tip_pos=[hands[0]["lmList"][4][0],hands[0]["lmList"][4][1]]
            forefinger_base_pos=[hands[0]["lmList"][5][0],hands[0]["lmList"][5][1]]
            forefinger_tip_pos=[hands[0]["lmList"][8][0],hands[0]["lmList"][8][1]]
            middle_finger_base_pos=[hands[0]["lmList"][9][0],hands[0]["lmList"][9][1]]
            middle_finger_tip_pos=[hands[0]["lmList"][12][0],hands[0]["lmList"][12][1]]
            cv2.circle(img, thumb_tip_pos, 6, (0, 0, 255), -1)
            cv2.circle(img, forefinger_base_pos, 6, (0, 0, 255), -1)
            cv2.circle(img, forefinger_tip_pos, 6, (0, 0, 255), -1)
            cv2.circle(img, middle_finger_base_pos, 6, (0, 0, 255), -1)
            cv2.circle(img, middle_finger_tip_pos, 6, (0, 0, 255), -1)
            ma_main.update_hand_pos(forefinger_tip_pos)
            ma_main.checkIfClicked(thumb_tip_pos, forefinger_base_pos, middle_finger_base_pos, middle_finger_tip_pos)
        except Exception as e:
            print(f"There was an error ! : {e}")

# ---------------------------------------------------------------
# |||||                 USE POINTS 4 5 8 9 12               |||||
# ---------------------------------------------------------------

    cv2.imshow('frame', img)
    key =cv2.waitKey(1)
    if key ==ord('q'):
        break

cv2.destroyAllWindows()