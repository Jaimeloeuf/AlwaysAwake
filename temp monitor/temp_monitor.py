import os
from asyncio import sleep
from JSutils import setInterval

# Global variable to save the delay time.
time = 4

def temp():
    # temp = os.popen("vcgencmd measure_temp").readline()
    # print(temp)
    # print(temp.replace("temp=", ""))
    print('30C') # Testing

# Create a loop that constantly prints the temperature.
loop = setInterval(time, temp)


# Infinite loop that runs to read user input
while True:
    # global loop
    try:
        option = input()
        if option == 'k':
            time = time + 0.25
        elif option == 'm':
            time = time - 0.25
        else:
            print('Invalid option entered')
    except:
        exit(0)
        



"""
When the user presses enter regardless of delay time, make and print another reading before going into delay again
User can press the keys:
    k: to speed up by 0.25 seconds
    m: to slow down by 0.25 seconds

"""