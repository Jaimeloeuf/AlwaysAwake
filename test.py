def foo(queue):
    from time import sleep
    while True:
        queue.put('hello')
        sleep(0.01)

def main():
    import multiprocessing as mp

    # Read the pipe, do the below only if image avail in the pipe

    # Use the 'spawn' method to start a new Process
    mp.set_start_method('spawn')
    # Create a new Queue object
    queue = mp.Queue()
    p = mp.Process(target=foo, args=(queue,))
    p.start()
    while True:
        while not queue.empty():
            print(queue.get())
    p.join()

if __name__ == "__main__":
    main()