from multiprocessing import Process
import os

# def cpu_task(n):
#     total = 0
#     for i in range(10_000_000):
#         total += i * i
#     print(f"Process {n}, PID={os.getpid()}, total={total}")

# if __name__ == "__main__":
#     p1 = Process(target=cpu_task, args=(1,))
#     p2 = Process(target=cpu_task, args=(2,))

#     p1.start()
#     p2.start()

#     p1.join()
#     p2.join()

#     print("Done")


# import threading
# import time

# def cpu_task():
#     total = 0
#     for i in range(30_000_000):
#         total += i * i

# start = time.time()

# t1 = threading.Thread(target=cpu_task)
# t2 = threading.Thread(target=cpu_task)

# t1.start()
# t2.start()

# t1.join()
# t2.join()

# print("Threads time:", time.time() - start)

from multiprocessing import Process
import time

def cpu_task():
    total = 0
    for i in range(30_000_000):
        total += i * i

if __name__ == "__main__":
    start = time.time()

    p1 = Process(target=cpu_task)
    p2 = Process(target=cpu_task)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Processes time:", time.time() - start)