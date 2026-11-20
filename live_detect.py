import cv2
import time
from ultralytics import YOLO
from detector import detect
from tracker import Tracker

ALLOWED_LABELS = ["person", "bicycle", "car", "motorcycle", "bus", "truck"]

cap = cv2.VideoCapture(0)

prev_time = time.time()

model = YOLO("yolo26n.pt")

tracker = Tracker()


while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame couldn't be read")
        break

    detections = detect(model,frame, allowed_labels=ALLOWED_LABELS)
    tracks = tracker.update(detections)
    pres_time = time.time()
    duration = pres_time - prev_time
    fps = 1 / duration
    prev_time = pres_time

    for track in tracks:
        if track.missed_frames == 0:
            cv2.rectangle(frame, (track.bbox.x1,track.bbox.y1), (track.bbox.x2, track.bbox.y2), (0, 255, 0), 2)
            cv2.putText(frame,f"{track.bbox.label}, ID: {track.ID}, conf: {track.bbox.confidence:.2f}", 
                        (track.bbox.x1, track.bbox.y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
      

    cv2.putText(frame,f"FPS: {fps:.1f}",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (255, 0, 0), 1)
    cv2.imshow("Webcam", frame)

    

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()