from  bounding_box import BoundingBox
class Track:
    def __init__(self, ID, bbox):
        self.ID = ID
        self.bbox = bbox
        self.missed_frames = 0  

    def update(self, new_box):
        self.bbox =  new_box
        self.missed_frames = 0


box = BoundingBox(10,20,30,40,"person")

box2 = BoundingBox(30,40,20,40,"car")

track_object = Track(20,box)

print(track_object.bbox.label, track_object.ID)

track_object.update(box2)

print(track_object.bbox.label, track_object.ID)
    

    
        