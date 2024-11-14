import cv2
import argparse

class ObjectTracker:
    OPENCV_OBJECT_TRACKERS = {
        'CSRT': cv2.TrackerCSRT_create if hasattr(cv2, 'TrackerCSRT_create') else None,
        'KCF': cv2.TrackerKCF_create if hasattr(cv2, 'TrackerKCF_create') else None
    }

    def __init__(self):
        self.args = self.parse_arguments()
        self.cap = cv2.VideoCapture(self.args["video"] or 1)
        self.cap.set(3, self.args["width"])
        self.cap.set(4, self.args["height"])
        self.tracker_type = self.args["tracker"].upper()
        self.tracker = None
        self.bbox = None
        self.fps = 0

    @staticmethod
    def parse_arguments():
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", type=str, help="Path to input video file")
        ap.add_argument("-t", "--tracker", type=str, default="KCF", help="OpenCV object tracker type")
        ap.add_argument("--width", type=int, default=800, help="Set video width")
        ap.add_argument("--height", type=int, default=600, help="Set video height")
        return vars(ap.parse_args())

    def create_tracker(self):
        if self.tracker_type not in self.OPENCV_OBJECT_TRACKERS or self.OPENCV_OBJECT_TRACKERS[self.tracker_type] is None:
            print(f"[WARNING] {self.tracker_type} is not available. Falling back to KCF")
            self.tracker_type = 'KCF'
        return self.OPENCV_OBJECT_TRACKERS[self.tracker_type]()

    def select_roi(self, frame):
        self.bbox = cv2.selectROI("Camera Feed", frame, False)
        if all(self.bbox):
            self.tracker = self.create_tracker()
            self.tracker.init(frame, self.bbox)

    def track_object(self, frame):
        if self.tracker:
            timer = cv2.getTickCount()
            success, self.bbox = self.tracker.update(frame)
            self.fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            if success:
                p1 = (int(self.bbox[0]), int(self.bbox[1]))
                p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
                cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)  # Changed color to green

    def display_info(self, frame):
        cv2.putText(frame, f"Tracker: {self.tracker_type}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 170, 50), 2)
        cv2.putText(frame, f"FPS: {int(self.fps)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 170, 50), 2)

    def switch_tracker(self, key, frame):
        index = key - ord('1')
        if 0 <= index < len(self.OPENCV_OBJECT_TRACKERS):
            self.tracker_type = list(self.OPENCV_OBJECT_TRACKERS.keys())[index]
            print(f"Switched to {self.tracker_type} tracker")
            if self.bbox:
                self.tracker = self.create_tracker()
                self.tracker.init(frame, self.bbox)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            if self.tracker:
                self.track_object(frame)
                self.display_info(frame)

            cv2.imshow("Camera Feed", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                self.select_roi(frame)
            elif ord('1') <= key <= ord('9'):
                self.switch_tracker(key, frame)

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    ObjectTracker().run()