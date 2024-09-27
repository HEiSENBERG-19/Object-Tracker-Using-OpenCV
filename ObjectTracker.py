import cv2
import argparse

class ObjectTracker:
    def __init__(self):
        self.cap = None
        self.bbox = None
        self.tracker = None
        self.tracking = False
        self.args = self.parse_arguments()
        self.tracker_type = self.args["tracker"].upper()
        self.fps = 0
        self.OPENCV_OBJECT_TRACKERS = self.get_available_trackers()
        self.tracker_keys = list(self.OPENCV_OBJECT_TRACKERS.keys())

    def parse_arguments(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", type=str, help="Path to input video file")
        ap.add_argument("-t", "--tracker", type=str, default="KCF", help="OpenCV object tracker type")
        return vars(ap.parse_args())

    def get_available_trackers(self):
        trackers = {}
        if hasattr(cv2, 'TrackerCSRT_create'):
            trackers['CSRT'] = cv2.TrackerCSRT_create
        if hasattr(cv2, 'TrackerKCF_create'):
            trackers['KCF'] = cv2.TrackerKCF_create
        if hasattr(cv2, 'TrackerMOSSE_create'):
            trackers['MOSSE'] = cv2.TrackerMOSSE_create
        if hasattr(cv2, 'TrackerBoosting_create'):
            trackers['BOOSTING'] = cv2.TrackerBoosting_create
        if hasattr(cv2, 'TrackerMIL_create'):
            trackers['MIL'] = cv2.TrackerMIL_create
        if hasattr(cv2, 'TrackerTLD_create'):
            trackers['TLD'] = cv2.TrackerTLD_create
        if hasattr(cv2, 'TrackerMedianFlow_create'):
            trackers['MEDIANFLOW'] = cv2.TrackerMedianFlow_create
        return trackers

    def create_tracker(self):
        if self.tracker_type not in self.OPENCV_OBJECT_TRACKERS:
            print(f"[WARNING] {self.tracker_type} is not available. Falling back to KCF")
            self.tracker_type = 'KCF'
        return self.OPENCV_OBJECT_TRACKERS[self.tracker_type]()

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

    def switch_tracker(self, key, frame):
        if ord('1') <= key <= ord(str(len(self.tracker_keys))):
            index = key - ord('1')
            if index < len(self.tracker_keys):
                self.tracker_type = self.tracker_keys[index]
                print(f"Switched to {self.tracker_type} tracker")
                if self.bbox is not None:
                    self.tracker = self.create_tracker()
                    self.tracker.init(frame, self.bbox)

    def run(self):
        if not self.args.get("video", False):
            print("[INFO] Starting video stream from webcam...")
            self.cap = cv2.VideoCapture(0)
        else:
            print(f"[INFO] Opening video file {self.args['video']}")
            self.cap = cv2.VideoCapture(self.args["video"])

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
            else:
                self.switch_tracker(key, frame)

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = ObjectTracker()
    tracker.run()