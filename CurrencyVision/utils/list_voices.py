import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for v in voices:
    print("ID:", v.id)
    print("Name:", v.name)
    print("Languages:", v.languages)
    print("-" * 30)
