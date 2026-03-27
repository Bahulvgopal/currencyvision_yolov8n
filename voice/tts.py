import pyttsx3
import threading

class VoiceEngine:
    def speak(self, text):
        def run():
            print("🔊 Speaking:", text)

            try:
                # 🔥 Create NEW engine every time (fixes silent bug)
                engine = pyttsx3.init(driverName='sapi5')
                engine.setProperty("rate", 170)
                engine.setProperty("volume", 1.0)

                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[0].id)

                engine.say(text)
                engine.runAndWait()
                engine.stop()

            except Exception as e:
                print("TTS Error:", e)

        threading.Thread(target=run, daemon=True).start()