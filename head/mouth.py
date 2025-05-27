import asyncio
import threading
import os
import edge_tts
import pygame

VOICE = "en-AU-WilliamNeural"

def remove_file(file_path):
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        try:
            with open(file_path, "wb"):
                pass

            os.remove(file_path)
            break
        except Exception as ex:
            print(f"Error: {ex}")
            attempts += 1

def play_audio(file_path):
    try:
        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound(file_path)
        sound.play()

        while pygame.mixer.get_busy():
            pygame.time.get_ticks()

        pygame.quit()
    except Exception as ex:
        print(f"Error: {ex}")

def speak(TEXT, output_file=None):
    if output_file is None:
        output_file = f"{os.getcwd()}/speak.mp3"
    
    asyncio.run(amain(TEXT, output_file))

async def amain(TEXT, output_file) -> None:
    try:
        comunnicate_text = edge_tts.Communicate(TEXT, VOICE)
        await comunnicate_text.save(output_file)
        thread = threading.Thread(target=play_audio, args=(output_file, ))
        thread.start()
        thread.join()
    except Exception as ex:
        print(f"Error: {ex}")
    finally:
        remove_file(output_file)
