import cv2

class ObjectTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.bbox = None
        self.tracker = None
        self.tracking = False
        self.tracker_type = 'KCF'
        self.tracker_types = ['KCF', 'CSRT', 'MOSSE']
        self.fps = 0

    def create_tracker(self):
        trackers = {
            'CSRT': cv2.legacy.TrackerCSRT_create,
            'KCF': cv2.legacy.TrackerKCF_create,
            'MOSSE': cv2.legacy.TrackerMOSSE_create
        }
        return trackers[self.tracker_type]()

    def select_roi(self, frame):
        self.bbox = cv2.selectROI("Camera Feed", frame, False)
        self.tracker = self.create_tracker()
        self.tracker.init(frame, self.bbox)
        self.tracking = True

    def track_object(self, frame):
        timer = cv2.getTickCount()
        success, self.bbox = self.tracker.update(frame)
        self.fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        if success:
            p1 = (int(self.bbox[0]), int(self.bbox[1]))
            p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

    def display_info(self, frame):
        cv2.putText(frame, f"Tracker: {self.tracker_type}", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 170, 50), 2)
        cv2.putText(frame, f"FPS: {int(self.fps)}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 170, 50), 2)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            if self.tracking:
                self.track_object(frame)
                self.display_info(frame)

            cv2.imshow("Camera Feed", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                self.select_roi(frame)
            elif key in [ord('1'), ord('2'), ord('3')]:
                self.tracker_type = self.tracker_types[int(key) - ord('1')]
                print(f"Switched to {self.tracker_type} tracker")
                if self.bbox is not None:
                    self.tracker = self.create_tracker()
                    self.tracker.init(frame, self.bbox)

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = ObjectTracker()
    tracker.run()