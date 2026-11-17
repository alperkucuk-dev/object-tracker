import cv2
import time

from bounding_box import BoundingBox

cap = cv2.VideoCapture(0)

box = BoundingBox(100, 100, 300, 300, "person")

prev_time = time.time()

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame couldn't be read")
        break

    pres_time = time.time()
    duration = pres_time - prev_time
    fps = 1 / duration
    prev_time = pres_time

    cv2.rectangle(frame, (box.x1,box.y1), (box.x2, box.y2), (0, 255, 0), 2)
    cv2.putText(frame, box.label, (box.x1, box.y2), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (0, 0, 255), 8)
    cv2.putText(frame, f"FPS: {fps:.1f}",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (255, 0, 0), 1)
    

    cv2.imshow("Webcam", frame)

    

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()