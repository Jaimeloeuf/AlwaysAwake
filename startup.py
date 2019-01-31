""" Dependencies """
from multiprocessing import Process


""" Module used to run the user test and setup files before starting the detection system """


# Run the detection system in another process and quit the current process used by the 'startup' module
def start_full_system():
    process = Process(target=)
    process.start()

    # Since the process is not set as a daemon, it will continue running even after this process exits.

    # Should I still join? I don't think should join since the process is an infinite loop. Which will preven the exit from being called.
    process.join()

    # Exit the current process
    exit(0)
