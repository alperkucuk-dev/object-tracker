from bounding_box import BoundingBox

def detect(model, frame, min_confidence=0.5, allowed_labels=None):
    detections = []
    results = model(frame, verbose=False) 

    

    result = results[0]

    for box in result.boxes:

        class_id = int(box.cls)
        confidence = float(box.conf)

        if confidence < min_confidence:
            continue

        x1,y1,x2,y2 = box.xyxy[0].tolist()
        label = model.names[class_id]

        if allowed_labels is not None and label not in allowed_labels:
            continue
            
            

        
        bbox = BoundingBox(x1, y1, x2, y2, label, confidence)
        detections.append(bbox)

    return detections


