import cv2
import numpy as np
import mediapipe as mp
import math
mp_face_mesh = mp.solutions.face_mesh

cap = cv2.VideoCapture(0)
cap.set(3, 1200)
cap.set(4, 720)

# indices d'iris
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

L_H_LEFT = [33]     # œil droit point de repère le plus à droite
L_H_RIGHT = [133]   # oeil droit point de repère le plus à gauche
R_H_LEFT = [362]    # œil gauche point de repère le plus à droite
R_H_RIGHT = [263]   # œil gauche point de repère le plus à gauche

#Fonction qui définit les distances euclidiennes des points dans les yeux
def euclidean_distance(point1, point2):
    x1, y1 =point1.ravel()
    x2, y2 =point2.ravel()
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance

#Fonction pour trouver la position de l'iris
def iris_position(iris_center, right_point, left_point):
    center_to_right_dist = euclidean_distance(iris_center, right_point)
    total_distance = euclidean_distance(right_point, left_point)
    ratio = center_to_right_dist/total_distance
    iris_position =""
    if ratio <= 0.42:
        iris_position="right"
    elif ratio > 0.42 and ratio <= 0.57:
        iris_position="center"
    else:
        iris_position = "left"
    return iris_position, ratio

with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   #Mediapipe a besoin du format de couleur RVB mais OpenCV utilise BGR
        img_h, img_w = frame.shape[:2]
        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])

            # transformer les formes carrées en cercles, la fonction OpenCV fournit des cercles de délimitation basés sur des points donnés.
            #minEnclosingCircle qui retourne, le centre (x,y) et le rayon des cercles, les valeurs de retour sont à virgule flottante, il faut les transformer en int.
            (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (r_cx,r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])

            # transformer les points centraux en tableau NP
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)

            #dessine le cercle en fonction des valeurs de retour de minEnclosingCircle, via CIRCLE qui dessine l'image du cercle en fonction du centre (x, y) et du rayon
            cv2.circle(frame, center_left, int(l_radius), (255, 0, 255), 1, cv2.LINE_AA)
            cv2.circle(frame, center_right, int(r_radius), (255, 0, 255), 1, cv2.LINE_AA)

            #montrer des points au coin des yeux
            cv2.circle(frame, mesh_points[R_H_RIGHT][0], 3, (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(frame, mesh_points[R_H_LEFT][0], 3, (0, 255, 255), -1, cv2.LINE_AA)

            cv2.circle(frame, mesh_points[L_H_RIGHT][0], 3, (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(frame, mesh_points[L_H_LEFT][0], 3, (0, 255, 255), -1, cv2.LINE_AA)

            iris_pos, ratio = iris_position(center_right, mesh_points[R_H_RIGHT], mesh_points[R_H_LEFT][0])

            print(f"iris in on the {iris_pos} position")
        cv2.imshow("img", frame)
        key = cv2.waitKey(1)
        if key ==ord("q"):
            break
cap.release()
cv2.destroyAllWindows()