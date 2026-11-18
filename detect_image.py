from ultralytics import YOLO

model = YOLO("yolo26n.pt")

results = model("https://ultralytics.com/images/bus.jpg")

result = results[0]

size = len(result.boxes)

print(size)

for box in  result.boxes:

    class_id = int(box.cls)
    confidence = float(box.conf)
    x1,y1,x2,y2 = box.xyxy[0].tolist()
    label = model.names[class_id]
    print(f"Label: {label}, confidence: {confidence:.2f}, "
    f"coordinates: ({x1:.0f}, {y1:.0f}), ({x2:.0f}, {y2:.0f}) ")





#print(result)

