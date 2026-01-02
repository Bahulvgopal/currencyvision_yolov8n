import speech_recognition as sr
import threading
import time

class VoiceCommandListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

        self.mode = "STOPPED"   # STOPPED | RUNNING
        self.reset_requested = False

        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.thread.start()

    def listen(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                with self.mic as source:
                    audio = self.recognizer.listen(source, phrase_time_limit=3)

                command = self.recognizer.recognize_google(audio).lower()
                print("🎤 Heard:", command)

                if "china" in command:
                    self.mode = "RUNNING"

                elif "exit" in command:
                    self.mode = "STOPPED"

                elif "reset" in command:
                    self.reset_requested = True

            except sr.UnknownValueError:
                pass
            except Exception as e:
                print("Voice error:", e)

            time.sleep(0.3)
