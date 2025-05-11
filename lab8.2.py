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

        for i, corner in enumerate(corners):
            center_x = int(corner[0][:, 0].mean())
            center_y = int(corner[0][:, 1].mean())

            cv2.putText(frame, f"X: {center_x}, Y: {center_y}",
                        (center_x + 10, center_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)

    cv2.imshow('Marker Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()