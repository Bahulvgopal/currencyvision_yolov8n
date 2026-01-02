import cv2
from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path="models/india.pt", conf=0.5):

        self.model = YOLO(model_path)
        self.conf = conf

    def detect(self, frame):
        """
        Takes a frame and returns:
        - annotated_frame
        - list of detected labels
        """
        results = self.model(frame, conf=self.conf, verbose=False)

        detected_labels = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                detected_labels.append(label)

        annotated_frame = results[0].plot()
        return annotated_frame, detected_labels
