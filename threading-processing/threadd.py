import threading
import time

def worker(name):
    print(f"{name} started")
    time.sleep(4)
    print(f"{name} finished")

t1 = threading.Thread(target=worker, args=("Thread-1",))
t2 = threading.Thread(target=worker, args=("Thread-2",))

t1.start()
t2.start()

t1.join()
t2.join()

print("Main finished")
