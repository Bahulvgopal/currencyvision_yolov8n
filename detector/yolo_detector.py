import cv2
from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path="models/india.pt", conf=0.65):
        self.model = YOLO(model_path)
        self.conf = conf

        self.allowed_labels = set([
            "INR_1", "INR_5", "INR_10", "INR_20",
            "INR_50", "INR_100", "INR_200", "INR_500",
            "INR_COIN_1", "INR_COIN_2", "INR_COIN_5",
            "INR_COIN_10", "INR_COIN_20"
        ])

    def detect(self, frame):
        results = self.model(frame, conf=self.conf, verbose=False)

        detected_labels = []
        annotated = frame.copy()

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                conf = float(box.conf[0])

                # ❌ Reject non-currency
                if label not in self.allowed_labels:
                    continue

                # ❌ Low confidence
                if conf < 0.65:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                width = x2 - x1
                height = y2 - y1
                area = width * height

                # ❌ Too small (paper text)
                if area < 10000:
                    continue

                # ❌ Wrong shape
                ratio = width / height if height != 0 else 0
                if ratio < 1.5 or ratio > 3.5:
                    continue

                detected_labels.append(label)

                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    annotated,
                    f"{label} ({conf:.2f})",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

        return annotated, detected_labels