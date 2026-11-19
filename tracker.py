from  bounding_box import BoundingBox

class Track:
    def __init__(self, ID, bbox):
        self.ID = ID
        self.bbox = bbox
        self.missed_frames = 0  

    def update(self, new_box):
        self.bbox =  new_box
        self.missed_frames = 0


class Tracker:
    def __init__(self, min_iou=0.3, max_missed_frames=10):
        self.min_iou = min_iou
        self.max_missed_frames = max_missed_frames        
        self.tracks = []
        self.next_ID = 1 

    def update(self, detections):
        
        for box in detections:
            best_track = None
            best_iou = 0
            for track in self.tracks:
                if track.bbox.label != box.label:
                    continue
               
                var_iou = track.bbox.iou(box)
                if var_iou > best_iou:
                    best_iou = var_iou
                    best_track = track

            if(best_iou >= self.min_iou):
                best_track.update(box)
                        
            








if __name__ == "__main__":
    box = BoundingBox(10,20,30,40,"person")
    box2 = BoundingBox(30,40,20,40,"car")   

    track_object = Track(20,box)
    print(track_object.bbox.label, track_object.ID)

    track_object.update(box2)
    print(track_object.bbox.label, track_object.ID)
    

    
        