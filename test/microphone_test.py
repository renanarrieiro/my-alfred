import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Diga alguma coisa...")
    audio = r.listen(source)
    print("Reconhecendo...")

try:
    text = r.recognize_google(audio, language="pt-BR")
    print("Você disse:", text)
except Exception as e:
    print("Erro:", e)