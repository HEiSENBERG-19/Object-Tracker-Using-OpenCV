import cv2
import argparse
import mediapipe as mp

class ObjectTracker:
    OPENCV_OBJECT_TRACKERS = {
        'CSRT': cv2.TrackerCSRT_create if hasattr(cv2, 'TrackerCSRT_create') else None,
        'KCF': cv2.TrackerKCF_create if hasattr(cv2, 'TrackerKCF_create') else None
    }

    def __init__(self):
        self.args = self.parse_arguments()
        self.cap = cv2.VideoCapture(self.args["video"] or 0)
        self.cap.set(3, self.args["width"])
        self.cap.set(4, self.args["height"])
        self.tracker_type = self.args["tracker"].upper()
        self.tracker = None
        self.bbox = None
        self.fps = 0

        # MediaPipe Hands setup
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

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

    def detect_hands_and_fingers(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Determine left or right hand
                hand_label = handedness.classification[0].label  # "Left" or "Right"

                # Finger counting logic
                fingers = []
                tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Little fingers

                # Thumb
                if hand_label == "Right":
                    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:
                    if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                # Other fingers
                for id in range(1, 5):
                    if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                finger_count = fingers.count(1)

                # Display the hand label and finger count
                cv2.putText(frame, f"{hand_label} Hand: {finger_count} Fingers", (10, 100 if hand_label == "Right" else 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 170, 50), 2)

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

            # Flip the frame horizontally to fix mirroring
            frame = cv2.flip(frame, 1)

            if self.tracker:
                self.track_object(frame)

            self.detect_hands_and_fingers(frame)
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