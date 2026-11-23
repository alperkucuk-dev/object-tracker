import cv2
import time
from ultralytics import YOLO
from detector import detect
from tracker import Tracker

ALLOWED_LABELS = ["person", "bicycle", "car", "motorcycle", "bus", "truck"]
VIDEO_SOURCE = "videos/traffic.mp4"

cap = cv2.VideoCapture(VIDEO_SOURCE)

video_fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter("videos/output.mp4", fourcc, video_fps,(width,height))


prev_time = time.time()

model = YOLO("yolo26n.pt")

tracker = Tracker()


while True:

    ret, frame = cap.read()

    if not ret:
        print("Video finished")
        break

    detections = detect(model,frame, allowed_labels=ALLOWED_LABELS, min_confidence=0.3)
    tracks = tracker.update(detections)
    pres_time = time.time()
    duration = pres_time - prev_time
    fps = 1 / duration
    prev_time = pres_time

    for track in tracks:
        if track.missed_frames == 0:
            cv2.rectangle(frame, (track.bbox.x1,track.bbox.y1), (track.bbox.x2, track.bbox.y2), (0, 255, 0), 2)
            cv2.putText(frame,f"{track.label()}, ID: {track.ID}, conf: {track.bbox.confidence:.2f}", 
                        (track.bbox.x1, track.bbox.y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
      

    cv2.putText(frame,f"FPS: {fps:.1f}",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (255, 0, 0), 1)

    y = 60

    for label, count in tracker.counts.items():
        cv2.putText(frame,f"{label}: {count}",(10, y), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (0, 255, 0), 1)
        y += 30
    
    cv2.imshow("Object Tracker", frame)
    writer.write(frame)


    

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
writer.release()
cv2.destroyAllWindows()