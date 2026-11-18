class BoundingBox:
    def __init__(self, x1, y1 ,x2, y2, label, confidence=1.0):
        self.x1 = round(x1)
        self.y1 = round(y1)
        self.x2 = round(x2)
        self.y2 = round(y2)
        self.label = label
        self.confidence = confidence

    
    
    def width(self):
        return self.x2 - self.x1 

    def height(self):
        return self.y2 - self.y1
    
    def area(self):
        return self.width() * self.height()

    def center(self):
        x_center = (self.x1 + self.x2) / 2
        y_center = (self.y1 + self.y2) / 2
        return x_center,y_center

    def iou(self,other):

        left_x = max(self.x1,other.x1)
        bottom_y = max(self.y1,other.y1)
        top_y = min(self.y2,other.y2)
        right_x = min(self.x2,other.x2)

        intersection_area = max((right_x - left_x),0) * max(0,(up_y - down_y))
        union_area = self.area() + other.area() - intersection_area

        IoU = intersection_area / union_area
        return IoU