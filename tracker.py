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
        matched_tracks = []
        new_tracks = []

        for box in detections:
            best_track = None
            best_iou = 0
            for track in self.tracks:
                if track.bbox.label != box.label:
                    continue

                if track in matched_tracks:
                    continue
               
                var_iou = track.bbox.iou(box)
                if var_iou > best_iou:
                    best_iou = var_iou
                    best_track = track

            if(best_iou >= self.min_iou):
                best_track.update(box)
                matched_tracks.append(best_track)

            else:
                new_track = Track(self.next_ID, box)
                self.next_ID += 1
                new_tracks.append(new_track)

        for new_track in new_tracks:
            self.tracks.append(new_track)   

            








if __name__ == "__main__":
    
    def print_tracks(frame_no, tracker):
        print(f"--- Frame {frame_no} ---")
        for track in tracker.tracks:
            print(f"#{track.ID} {track.bbox.label} "
                  f"x1={track.bbox.x1} missed={track.missed_frames}")

    tracker = Tracker()

    
    frame1 = [BoundingBox(100, 100, 200, 300, "person")]
    tracker.update(frame1)
    print_tracks(1, tracker)

    
    frame2 = [BoundingBox(110, 100, 210, 300, "person")]
    tracker.update(frame2)
    print_tracks(2, tracker)

   
    frame3 = [
        BoundingBox(120, 100, 220, 300, "person"),
        BoundingBox(400, 100, 500, 300, "person"),
    ]
    tracker.update(frame3)
    print_tracks(3, tracker)
    

    
        