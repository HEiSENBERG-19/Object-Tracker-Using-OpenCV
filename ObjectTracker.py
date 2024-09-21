import cv2

class ObjectTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.bbox = None

    def select_roi(self, frame):
        self.bbox = cv2.selectROI("Camera Feed", frame, False)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            if self.bbox:
                p1 = (int(self.bbox[0]), int(self.bbox[1]))
                p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

            cv2.imshow("Camera Feed", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                self.select_roi(frame)

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = ObjectTracker()
    tracker.run()
