import cv2
import yaml
import sys
import os

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

# ---------------- EVENT STATE ----------------
currency_visible = False
absence_frames = 0
ABSENCE_REQUIRED = 10

voice.speak("Say china to begin currency detection")

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    annotated, labels = detector.detect(frame)

    # ---------- RESET ----------
    if commands.reset_requested:
        calculator.reset()
        currency_visible = False
        absence_frames = 0
        voice.speak("Total amount reset to zero")
        commands.reset_requested = False

    # ---------- STOP MODE ----------
    if commands.mode == "STOPPED":
        currency_visible = False
        absence_frames = 0

        cv2.putText(
            annotated,
            "Detection stopped",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )
        cv2.imshow("Currency Detection System", annotated)
        if cv2.waitKey(1) == 27:
            break
        continue

    # ---------- FILTER VALID LABELS ----------
    valid = [
        l for l in labels
        if l in currency_cfg["notes"] or l in currency_cfg["coins"]
    ]

    # ---------- EVENT-BASED COUNTING ----------
    if not valid:
        absence_frames += 1
        if absence_frames >= ABSENCE_REQUIRED:
            currency_visible = False
    else:
        absence_frames = 0

        if not currency_visible:
            label = valid[0]
            value = currency_cfg["notes"].get(label) or currency_cfg["coins"].get(label)

            calculator.add_currency(label, value)

            voice.speak(
                lang_mgr.detected_text(value)
                + ". "
                + lang_mgr.total_text(calculator.get_total())
            )

            currency_visible = True

    # ---------- DISPLAY ----------
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
