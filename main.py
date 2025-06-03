
from functions.welcome import greeting
from head.ear import listen
from head.brain import think

if __name__ == "__main__":
    lisining = False

    while True:
        text_spoke = 'a'
        text_spoke = (listen() or "").lower()

        if text_spoke == "alfred":
            greeting()
            lisining = True
        if lisining == True:
            lisining = False
            print(think())