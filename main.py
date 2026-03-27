import cv2
import yaml
import sys
import os
import time
from collections import deque

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from detector.yolo_detector import YOLODetector
from logic.calculator import CurrencyCalculator
from voice.language import LanguageManager
from voice.tts import VoiceEngine
from voice.commands import VoiceCommandListener

# ---------------- LOAD CONFIG ----------------
with open("config/settings.yaml", encoding="utf-8") as f:
    settings = yaml.safe_load(f)

with open("config/currencies.yaml", encoding="utf-8") as f:
    currencies = yaml.safe_load(f)

country = settings["default_country"]
language = settings["default_language"]
camera_index = settings["camera_index"]

currency_cfg = currencies[country]

# ---------------- INIT ----------------
detector = YOLODetector(
    model_path=currency_cfg["model"],
    conf=settings["confidence_threshold"]
)

calculator = CurrencyCalculator()
lang_mgr = LanguageManager(language)
voice = VoiceEngine()
commands = VoiceCommandListener()

cap = cv2.VideoCapture(camera_index)

# ---------------- STATE ----------------
absence_frames = 0
ABSENCE_REQUIRED = 10

detection_active = False
last_spoken = 0
last_announced = None

def safe_speak(text):
    global last_spoken

    if time.time() - last_spoken < 0.5:
        return

    last_spoken = time.time()
    voice.speak(text)

recent_detections = deque(maxlen=5)

safe_speak("Say china to begin currency detection")

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ---------- COMMAND HANDLING ----------
    if commands.mode == "RUNNING":
        detection_active = True

    if commands.mode == "STOPPED":
        detection_active = False
        absence_frames = 0
        recent_detections.clear()
        last_announced = None

    # ---------- DETECTION ----------
    if detection_active:
        frame_small = cv2.resize(frame, (640, 480))
        annotated, labels = detector.detect(frame_small)
    else:
        annotated = frame.copy()
        labels = []

    # ---------- RESET ----------
    if commands.reset_requested:
        calculator.reset()
        absence_frames = 0
        recent_detections.clear()
        last_announced = None
        safe_speak("Total amount reset to zero")
        commands.reset_requested = False

    # ---------- FILTER VALID ----------
    valid = [
        l for l in labels
        if l in currency_cfg["notes"] or l in currency_cfg["coins"]
    ]

    # ---------- CONSISTENCY ----------
    if valid:
        recent_detections.append(valid[0])
    else:
        recent_detections.append(None)

    stable_label = None

    if len(recent_detections) == 5:
        counts = {}
        for item in recent_detections:
            if item:
                counts[item] = counts.get(item, 0) + 1

        if counts:
            best = max(counts, key=counts.get)
            if counts[best] >= 3:
                stable_label = best

    # ---------- SPEAK + COUNT ----------
    if stable_label is not None and stable_label != last_announced:
        value = currency_cfg["notes"].get(stable_label) or currency_cfg["coins"].get(stable_label)

        calculator.add_currency(stable_label, value)

        safe_speak(
            lang_mgr.detected_text(value)
            + ". "
            + lang_mgr.total_text(calculator.get_total())
        )

        last_announced = stable_label

    # ---------- ONE-LINE STATUS (NO SPAM) ----------
    status = f"MODE: {commands.mode} | DETECTION: {detection_active} | STABLE: {stable_label} | LAST: {last_announced}"
    sys.stdout.write("\r" + status)
    sys.stdout.flush()

    # ---------- DISPLAY ----------
    if detection_active:
        cv2.putText(
            annotated,
            "DETECTION ACTIVE",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.putText(
        annotated,
        f"Total: {calculator.get_total()}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Currency Detection System", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()