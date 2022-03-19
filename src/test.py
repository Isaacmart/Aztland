from threading import Thread
from threading import Lock

lock = Lock()


def test():
    print("Thread started")
    for i in range(50):
        print(i)
    print("Thread finished")


def thread_test():
    for i in range(5):
        thread = Thread(target=test)
        thread.start()
        thread.join()
        print("after join")
    print("Thread is done")


thread_test()

