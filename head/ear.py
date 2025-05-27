import speech_recognition as sr
import os
import multiprocessing as mp
from deep_translator import GoogleTranslator
from colorama import Fore, Style, init

init(autoreset=True)

def trans_pt_to_en(text):
    try:
        english_text = GoogleTranslator(source="pt", target="en").translate(text)
        return english_text
    except Exception as e:
        print(Fore.RED + f"[ERROR] Translation failed: {e}")
        return ""

def listen_and_translate():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 3000
    recognizer.pause_threshold = 2.5

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print(Fore.GREEN + "I am listening...")

        while True:
            try:
                print(Fore.GREEN + "\nSpeak something:")
                audio = recognizer.listen(source)
                print(Fore.YELLOW + "Processing...")

                recognized_text = recognizer.recognize_google(audio, language="pt-BR")
                print(Fore.WHITE + f"\nYou said: {recognized_text}")

                translated_text = trans_pt_to_en(recognized_text)
                print(Fore.CYAN + f"Translation (EN): {translated_text}")

            except sr.UnknownValueError:
                print(Fore.RED + "Could note understand audio.")

            except sr.RequestError as ex:
                print(Fore.RED + f"API error: {ex}")

            except KeyboardInterrupt:
                print(Fore.MAGENTA + "/n[Stopped by user]")

def main():
    process = mp.Process(target=listen_and_translate)
    process.start()
    try:
        process.join()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[Main Process] Interrupt received. Terminating child process...")
        process.terminate()
        process.join()


if __name__ == "__main__":
    mp.set_start_method("spawn")
    os.system("cls" if os.name == "nt" else "clear")
    main()
