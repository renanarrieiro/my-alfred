
from functions.welcome import greeting
from head.ear import listen
from head.brain import think
from data.dialog_data.wake_key_words import wake_key_words

if __name__ == "__main__":
    lisining = False

    while True:
        text_spoke = 'a'
        text_spoke = (listen() or "").lower()

        if text_spoke.replace(" ", "") in wake_key_words:
            greeting()
            lisining = True
            
        if lisining == True:
            lisining = False
            print(think())