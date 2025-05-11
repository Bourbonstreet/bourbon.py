import cv2
import numpy as np


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
marker_id = 0
marker_size = 400
marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
cv2.imwrite(r"C:\Users\CHRISTOPHER'M\Desktop\marker.png", marker_img)

cap = cv2.VideoCapture(0)
detector = cv2.aruco.ArucoDetector(aruco_dict)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    corners, ids, _ = detector.detectMarkers(frame)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        y_offset = 30
        for i in range(len(ids)):
            marker_corners = corners[i][0]

            center_x = int(marker_corners[:, 0].mean())
            center_y = int(marker_corners[:, 1].mean())

            text = f"ID {ids[i][0]}: X={center_x}, Y={center_y}"

            cv2.putText(frame, text, (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)
            y_offset += 30

    cv2.imshow('Marker Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()