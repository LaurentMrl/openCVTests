import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import math
import numpy as np
import cvzone
 
# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
 
# Hand Detector
detector = FaceMeshDetector(minDetectionCon=0.8)
 
# Find Function
# x is the raw distance y is the value in cm
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C
 
# Loop
compteur=0
while True:
    success, img = cap.read()
    face=detector.findFaceMesh(img, draw=False)
    if face[1]:
        # if compteur==0:
            # print(face[1][0])
        points_to_draw=[152, 377, 400, 378, 379, 365, 397, 367, 435, 401, 366, 434]
        for point in points_to_draw:
            cv2.circle(img,face[1][0][point], 6, (0, 0, 255), -1)
            
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    key = cv2.waitKey(1)
    if key ==ord("q"):
        break

# 152, 377, 400, 378, 379, 365, 397, 367, 435, 401, 366, 434