from bounding_box import BoundingBox

def detect(model, frame):
    detections = []
    results = model(frame) 

    result = results[0]

    for box in result.boxes:

        class_id = int(box.cls)
        confidence = float(box.conf)
        x1,y1,x2,y2 = box.xyxy[0].tolist()
        label = model.names[class_id]
        bbox = BoundingBox(x1, y1, x2, y2, label, confidence)
        detections.append(bbox)

    return detections


