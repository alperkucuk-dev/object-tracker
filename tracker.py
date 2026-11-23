from  bounding_box import BoundingBox

class Track:
    def __init__(self, ID, bbox):
        self.ID = ID
        self.bbox = bbox
        self.missed_frames = 0  
        self.hits = 1
        self.is_counted = False
        self.label_votes = {bbox.label : 1}
        

    def update(self, new_box):
        self.bbox =  new_box
        self.missed_frames = 0
        self.hits += 1
        if new_box.label in self.label_votes:
            self.label_votes[new_box.label] += 1
        else:
            self.label_votes[new_box.label] = 1

    def label(self):
        best_label = None
        most_votes = 0
        for vote in self.label_votes:
            if self.label_votes[vote] > most_votes:
                most_votes = self.label_votes[vote]
                best_label = vote
        return best_label

class Tracker:
    def __init__(self, min_iou=0.3, max_missed_frames=10, min_hits=3):
        self.min_iou = min_iou
        self.max_missed_frames = max_missed_frames        
        self.tracks = []
        self.next_ID = 1 
        self.counts = {}
        self.min_hits = min_hits
       

    def update(self, detections):
        matched_tracks = []
        new_tracks = []
        remaining_tracks = []

        for box in detections:
            best_track = None
            best_iou = 0
            for track in self.tracks:
                
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
                

        for track in self.tracks:
            if track not in matched_tracks:
                track.missed_frames += 1

            if track.missed_frames > self.max_missed_frames:
                continue

            remaining_tracks.append(track)
            
        self.tracks = remaining_tracks

        for new_track in new_tracks:
            self.tracks.append(new_track)   

        for track in self.tracks:

            if track.hits >= self.min_hits and not track.is_counted :
                if track.label() in self.counts:
                    self.counts[track.label()] += 1
                else:
                     self.counts[track.label()] = 1

                track.is_counted = True 
                            
                                    
       
        return self.tracks

            








if __name__ == "__main__":
    
    def print_tracks(frame_no, tracker):
        print(f"--- Frame {frame_no} ---")
        for track in tracker.tracks:
            print(f"#{track.ID} {track.label()} "
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

    for frame_no in range(4, 16):
        x = 120 + (frame_no - 3) * 5
        tracker.update([BoundingBox(x, 100, x + 100, 300, "person")])
        print_tracks(frame_no, tracker)
        print(tracker.counts)

       
    vote_tracker = Tracker()
    labels = ["car", "car", "truck", "car", "truck", "car", "car"]
    for i, label in enumerate(labels):
        x = 100 + i * 5
        vote_tracker.update([BoundingBox(x, 100, x + 100, 200, label)])
    for track in vote_tracker.tracks:
        print(f"#{track.ID} votes={track.label_votes} label={track.label()}")
    print(vote_tracker.counts)

    
        