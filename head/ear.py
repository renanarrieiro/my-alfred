import speech_recognition as sr
import os
import threading
from mtranslate import translate
from colorama import Fore, Style, init

init(autoreset=True)

def print_loop():
    while True:
        print(Fore.GREEN + "I am listing...", end="", flush=True)
        print(Style.RESET_ALL, end="", flush=True)
        print("", end="", flush=True)

def trans_pt_to_en(text):
    english_text = translate(text, to_language="en-US")
    return english_text

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False # Representa o limite do nível de energia para sons dinamicamente.
    recognizer.energy_threshold = 3000 # Representa o limite do nível de energia para sons.
    recognizer.dynamic_energy_adjustment_damping = 0.15 # Fração do limite de energia atual que é retida após um segundo de ajuste do limite dinâmico
    #recognizer.dynamic_energy_ratio = 1.9
    recognizer.pause_threshold = 2.5 # Representa a duração mínima do silêncio (em segundos) que será registrado como o final de uma frase
    recognizer.operation_timeout = None # Representa o tempo limite (em segundos) para operações internas, como solicitações de API.
    #recognizer.non_speaking_duration = 0.1

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            print(Fore.GREEN + "I am listing...\r", end="", flush=True)
            try:
                audio = recognizer.listen(source, timeout=None)
                print("\r" + Fore.YELLOW + "Got it, now recognizing", end="clear", flush=True)
                recognized_text = recognizer.recognize_google(audio, language="pt-BR").lower()
                if recognized_text:
                    translated_text = trans_pt_to_en(recognized_text)
                    print("\r" + Fore.BLUE + "Mr Renan: " + translated_text, end="", flush=True)
                    return translated_text
                else:
                    return ""
            except sr.UnknownValueError:
                recognized_text = ""
            finally:
                print("\r", end="", flush=True)

            os.system("cls" if os.name == "nt" else "clear")

            # threading part
            listen_thread = threading.Thread(target=listen)
            print_thread = threading.Thread(target=print_loop)
            listen_thread.start()
            print_thread.start()
            listen_thread.join()
            print_thread.join()
