import cv2
import time
from ultralytics import YOLO
from detector import detect
from bounding_box import BoundingBox

ALLOWED_LABELS = ["person", "bicycle", "car", "motorcycle", "bus", "truck"]

cap = cv2.VideoCapture(0)

prev_time = time.time()

model = YOLO("yolo26n.pt")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame couldn't be read")
        break

    detections = detect(model,frame, allowed_labels=ALLOWED_LABELS)
    pres_time = time.time()
    duration = pres_time - prev_time
    fps = 1 / duration
    prev_time = pres_time

    for box in detections:
        cv2.rectangle(frame, (box.x1,box.y1), (box.x2, box.y2), (0, 255, 0), 2)
        cv2.putText(frame,f"{box.label} conf: {box.confidence:.2f}", (box.x1, box.y1-10), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (0, 0, 255), 2)
      

    cv2.putText(frame,f"FPS: {fps:.1f}",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (255, 0, 0), 1)
    cv2.imshow("Webcam", frame)

    

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()