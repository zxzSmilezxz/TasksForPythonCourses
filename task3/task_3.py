from threading import Lock, Thread

a = 0
lock = Lock()

def function(arg):
    global a
    global l
    i = 0

    for _ in range(arg):
        i += 1
        
    lock.acquire()
    a += i
    lock.release()


def main():
    threads = []
    for i in range(5):
        thread = Thread(target=function, args=(1000000,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    print("----------------------", a)  # ???


main()
