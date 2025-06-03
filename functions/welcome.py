import datetime
import random
from head.mouth import speak
from data.dialog_data.greetings import *

current_hour = datetime.datetime.now().hour

def greeting():
    if 7 <= current_hour <= 11:
        speak(random.choice(dialog_good_morning))
    elif 12 <= current_hour <= 18:
        speak(random.choice(dialog_good_afternoon))
    else: 
        speak(random.choice(dialog_good_night))
    