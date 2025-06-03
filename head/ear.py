import speech_recognition as sr
import os
import time
import multiprocessing as mp
from deep_translator import GoogleTranslator
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# def translate_pt_to_en(text):
#     """
#     Translate Portuguese text to English with improved error handling.
    
#     Args:
#         text (str): Portuguese text to translate
        
#     Returns:
#         str: English translation or empty string if translation fails
#     """
#     if not text.strip():  # Handle empty or whitespace-only text
#         return ""
    
#     try:
#         # Create translator instance and perform translation
#         translator = GoogleTranslator(source="pt", target="en")
#         english_text = translator.translate(text)
#         return english_text if english_text else ""
        
#     except Exception as e:
#         print(Fore.RED + f"[ERROR] Translation failed: {e}")
#         # Return original text as fallback so user doesn't lose their input
#         print(Fore.YELLOW + f"[FALLBACK] Original text: {text}")
#         return ""
    
def setup_recognizer():
    """
    Configure and return a speech recognizer with optimized settings.
    
    Returns:
        sr.Recognizer: Configured recognizer instance
    """
    recognizer = sr.Recognizer()
    
    # Disable dynamic energy threshold for more consistent recognition
    recognizer.dynamic_energy_threshold = True
    # Set energy threshold (adjust based on your environment)
    #recognizer.energy_threshold = 3000
    # Set pause threshold (how long to wait for silence before processing)
    recognizer.pause_threshold = 2.0
    # Set timeout for listening (prevents hanging indefinitely)
    #recognizer.phrase_time_limit = 10  # 10 seconds max per phrase
    
    return recognizer

def listen():
    """
    Main function that continuously listens for speech, recognizes it,
    and translates from Portuguese to English.
    """
    recognizer = setup_recognizer()

    # Initialize microphone once outside the loop for better performance
    microphone = sr.Microphone()

    print(Fore.GREEN + "🎤 Speech Recognition and Translation Tool")
    print(Fore.GREEN + "📝 Speak in Portuguese, get English translation")
    print(Fore.YELLOW + "Press Ctrl+C to stop\n")

    # Adjust for ambient noise once at startup
    print(Fore.CYAN + "Calibrating microphone for ambient noise...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
    print(Fore.GREEN + "✓ Calibration complete!\n")

    while True:
        try:
            print(Fore.GREEN + "🔊 Listening... (speak now)")
            
            # Listen for audio with timeout to prevent hanging
            with microphone as source:
                try:
                    # Listen with timeout to avoid infinite waiting
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=10)
                except sr.WaitTimeoutError:
                    # If no speech detected, continue loop (avoids spam)
                    continue
            
            # print(Fore.YELLOW + "⏳ Processing speech...")
              # Recognize speech using Google's service
            try:
                recognized_text = recognizer.recognize_google(audio, language="pt-BR")
                # print(Fore.WHITE + f"🗣️  You said: {recognized_text}")

                return f"{recognized_text}"
                
                # Translate the recognized text
                # print(Fore.CYAN + "🔄 Translating...")
                # translated_text = translate_pt_to_en(recognized_text)
                
                # if translated_text:
                #     print(Fore.CYAN + f"🌍 Translation (EN): {translated_text}")
                # else:
                #     print(Fore.RED + "❌ Translation unavailable")
                    
                #print("-" * 50)  # Visual separator
                
            except sr.UnknownValueError:
                print(Fore.RED + "❓ Could not understand audio. Please speak clearly.")
                
            except sr.RequestError as ex:
                print(Fore.RED + f"🌐 Google Speech Recognition API error: {ex}")
                # print(Fore.YELLOW + "💡 Check your internet connection")

        except KeyboardInterrupt:
            # print(Fore.MAGENTA + "\n👋 Goodbye! Stopping speech recognition.")
            break
            
        except Exception as e:
            # print(Fore.RED + f"❌ Unexpected error: {e}")
            # print(Fore.YELLOW + "🔄 Continuing to listen...")
            # Add small delay to prevent rapid error loops
            time.sleep(1)
    
# def main():
#     """
#     Main entry point - simplified without unnecessary multiprocessing.
#     """
#     try:
#         # Clear screen for clean start
#         os.system("cls" if os.name == "nt" else "clear")
        
#         # Start the main listening loop
#         listen()
        
#     except KeyboardInterrupt:
#         print(Fore.RED + "\n🛑 Program interrupted by user")
#     except Exception as e:
#         print(Fore.RED + f"❌ Fatal error: {e}")

# if __name__ == "__main__":
#     main()
