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

class MyMouse():
    def __init__(self):
        print("init MyMouse")
        self.left_click=None
        self.right_click=None
        self.last_left_click=time.time()
    
    def update_mouse_pos(self, new_mouse_position):
        PAG.moveTo(new_mouse_position, _pause=False)

    def update_mouse_click(self, new_left_click, new_right_click):
        if new_left_click==True and self.left_click!=True:
            self.last_left_click=time.time()
            print("Left click")
            self.left_click=True
            mouse.press(Button.left)
        elif new_left_click==False and self.left_click!=False:
            print("left release")
            self.left_click=False
            mouse.release(Button.left)
        # if new_right_click==True and self.right_click!=True:
        #     self.new_right_click=time.time()
        #     print("Right click")
        #     self.right_click=True
        #     mouse.press(Button.right)
        # elif new_right_click==False and self.right_click!=False:
        #     print("Right release")
        #     self.right_click=False
        #     mouse.release(Button.right)



class MyHand():
    def __init__(self):
        print("Init MyHand")
        self.my_mouse=MyMouse()
    
    def update_hand_pos(self, new_forefinger_position):
        self.my_mouse.update_mouse_pos(new_forefinger_position)

def checkIfClicked(thumb_tip_pos, forefinger_base_pos, middle_finger_base_pos, middle_finger_tip_pos):
    if thumb_tip_pos[0]-forefinger_base_pos[0]>=-55:
        left_click=True
    else:
        left_click=False
    if middle_finger_tip_pos[1]-middle_finger_base_pos[1]>=-100:
        right_click=True
    else:
        right_click=False
    ma_main.my_mouse.update_mouse_click(left_click, right_click)


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
            # print(type(hands[0]["lmList"][4][0]))
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
            if time.time()-ma_main.my_mouse.last_left_click>=0.5:
                ma_main.update_hand_pos(forefinger_tip_pos)
            checkIfClicked(thumb_tip_pos, forefinger_base_pos, middle_finger_base_pos, middle_finger_tip_pos)
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