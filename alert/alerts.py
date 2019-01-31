""" Module used to alert the device user about events, as the device will be operating in Headless more. """
import gpiozero
# TTS library dependency
from espeak import espeak


# Function to alert user if eyes are in frame or not
def positioning(in_frame):
    if in_frame:
        return espeak.synth("Eyes detected in frame.")
    espeak.synth("Eyes not detected in the current frame")


# Sound on starting the detection system
def on_startup():
    espeak.synth("Detection System now running.")


def alert(text='alert'):
    if text == 'alert':
        espeak.synth("ALERT! WAKE UP!")
        # Activate the other alerts too like play sound from buzzer after the synth call.
    elif text == 'alert':
        pass


        # If this module is called as a standalone module to run, then execute the example code
if __name__ == "__main__":
    espeak.synth("Hello World!")


""" How to set output volume
    Since I assume that all this espeak synth calls are blocking calls, should all these be ran in a seperate process?
    But since the library is written in C, shouldn't it be already running in another process.
    """
