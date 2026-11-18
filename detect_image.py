from ultralytics import YOLO
from detector import detect

model = YOLO("yolo26n.pt")

detections = detect(model,"https://ultralytics.com/images/bus.jpg")

for bbox in detections:
    label = bbox.label
    confidence = bbox.confidence
    area = bbox.area()

    print(f"Label: {label}, confidence: {confidence:.2f}, area: {area}")