♿ CurrencyVision – Voice-Assisted Currency Detection System

CurrencyVision is an AI-powered assistive system designed to help visually impaired users identify currency denominations and calculate the total amount using computer vision and voice feedback.
The system uses YOLO-based object detection to recognize currency notes and provides real-time spoken output, along with voice commands for hands-free operation.

📌 Features

-📷 Real-time currency detection using camera

-🧠 Accurate total calculation, including repeated denominations

-🔊 Text-to-Speech (TTS) output for detected currency and total sum

-🎤 Voice commands:

            -china – begin detection ( you can change it in command.py file )

            -exit – pause detection ( you can change it in command.py file )

            -Reset – reset total amount to zero  ( you can change it in command.py file )

-♿ Assistive design suitable for blind and visually impaired users

-🧩 Modular architecture (easy to upgrade for more currencies & languages)

🛠️ Technologies Used

-Python 3.9+

-YOLO (Object Detection)

-OpenCV

-pyttsx3 (Text-to-Speech)

-SpeechRecognition (Voice Commands)

-PyAudio

-NumPy

-PyYAML

🧠 System Architecture

                Camera

                  ↓
  
          YOLO Currency Detector

                   ↓
  
        Event-Based Counting Logic

                    ↓
  
           Currency Calculator

                    ↓
  
           Text-to-Speech Output

                     ↑
  
    Voice Command Listener (Start / Stop / Reset)

📂 Project Structure

    CurrencyVision/
    │
    ├── main.py                     # Main application
    │
    ├── detector/
    │   └── yolo_detector.py        # YOLO inference logic
    │
    ├── logic/
    │   └── calculator.py           # Currency sum calculation
    │
    ├── voice/
    │   ├── tts.py                  # Text-to-speech (queued, thread-safe)
    │   ├── commands.py             # Voice command recognition
    │   └── language.py             # Language phrases
    │
    ├── config/
    │   ├── settings.yaml           # General settings
    │   └── currencies.yaml         # Currency definitions
    │
    ├── models/
    │   └── india.pt                # Trained YOLO model
    │
    ├── requirements.txt
    └── README.md



⚙️ Installation


1️⃣ Clone the Repository

    git clone https://github.com/your-username/CurrencyVision.git
    cd CurrencyVision

2️⃣ Create Virtual Environment (Recommended)

    python -m venv venv
    venv\Scripts\activate   # Windows

3️⃣ Install Dependencies

    pip install -r requirements.txt

⚠️ If PyAudio fails on Windows:

    pip install pipwin
    pipwin install pyaudio

▶️ How to Run

    python main.py

👉 Designed to run locally on the user’s device

🚀 Future Enhancements :

-🌍 Multi-currency support (USD, EUR, etc.)

-🪙 Coin detection

-🌐 Multi-language voice output

-📱 Android application version

-🧪 Fake currency detection

-📴 Offline speech recognition
