import pyttsx3
import threading

class VoiceEngine:
    def speak(self, text):
        def run():
            engine = pyttsx3.init()
            engine.setProperty("rate", 170)
            voices = engine.getProperty('voices')
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)
            engine.say(text)
            engine.runAndWait()

        threading.Thread(target=run, daemon=True).start()
import pyttsx3
import threading

class VoiceEngine:
    def speak(self, text):
        def run():
            engine = pyttsx3.init()
            engine.setProperty("rate", 170)
            voices = engine.getProperty('voices')
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)
            engine.say(text)
            engine.runAndWait()

        threading.Thread(target=run, daemon=True).start()
