import signal
import os
from gpiozero import CPUTemperature
from JSutils import setInterval
from Jevents import Watch


"""
When the user presses enter regardless of delay time, make and print another reading before going into delay again
User can press the keys:
    k: to speed up by 0.25 seconds
    m: to slow down by 0.25 seconds


Todo:
    Maybe run the read temperature and keyboard capture in seperate processes in order to keep
    main process clean and neat.
    Implement the NCurses lib or smth similiar for reading the input
"""


# Global variable to save the delay time.
time = Watch(4)
time.on_change += restart_loop


def read_temp():
    # temp = os.popen("vcgencmd measure_temp").readline()
    # print(temp)
    # print(temp.replace("temp=", ""))
    print('30C')  # Testing

    # Below is the RPi GPIOZERO's implementation of reading CPU temp values
    cpu = CPUTemperature()
    cpu.temperature


# Global variable holding the reference to the loop that constantly reads and prints the temperature.
loop = setInterval(time, read_temp)


def restart_loop(new_time):
    # Reference and use the global variable loop inside this scope block
    global loop
    # Stop the loop first
    loop.stop(True)
    # Assign a new loop with the new time
    loop = setInterval(new_time, read_temp)


# Infinite loop that runs to read user input
while True:
    """ How to read keyboard input and not print to screen """
    option = input()
    if option == 'k':
        time = time + 0.25
    elif option == 'm':
        time = time - 0.25
    else:
        print('Invalid option entered')


# Interrupt Signal handler
def signal_handler(signal, frame):
    print("Program interrupted!")
    # Stop the loop temperature reading loop on keyboard interrupt
    loop.stop()
    exit(0)


# Pass in the signal_handler to run when the INTerrupt signal is received
signal.signal(signal.SIGINT, signal_handler)
