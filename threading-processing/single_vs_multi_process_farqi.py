import time
import os
from multiprocessing import Process, Queue, cpu_count


def count_sum(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total


def run_single_process(tasks: list[int]):
    print("\n=== SINGLE PROCESS ===")
    start = time.perf_counter()

    results = []
    for n in tasks:
        pid = os.getpid()
        print(f"[PID={pid}] computing n={n}")
        results.append(count_sum(n))

    elapsed = time.perf_counter() - start
    print(f"SINGLE PROCESS total time: {elapsed:.3f}s")
    return results


def worker(n: int, q: Queue):
    pid = os.getpid()
    start = time.perf_counter()
    result = count_sum(n)
    elapsed = time.perf_counter() - start
    q.put({
        "pid": pid,
        "n": n,
        "result": result,
        "time": elapsed,
    })


def run_multi_processing(tasks: list[int]):
    print("\n=== MULTIPROCESSING ===")
    start = time.perf_counter()

    processes = []
    q = Queue()

    for n in tasks:
        p = Process(target=worker, args=(n, q))
        processes.append(p)
        p.start()

    results = []
    for _ in tasks:
        results.append(q.get())

    for p in processes:
        p.join()

    elapsed = time.perf_counter() - start

    for item in results:
        print(
            f"[PID={item['pid']}] computed n={item['n']} | "
            f"worker_time={item['time']:.3f}s"
        )

    print(f"MULTIPROCESSING total time: {elapsed:.3f}s")
    return results


if __name__ == "__main__":
    print(f"CPU cores available: {cpu_count()}")

    # Mashinangga qarab bu sonni oshir/pasaytir.
    # Juda kichik bo‘lsa farq bilinmaydi, juda katta bo‘lsa laptopni qiynaydi.
    TASKS = [20_000_000, 20_000_000, 20_000_000, 20_000_000]

    # run_single_process(TASKS)
    run_multi_processing(TASKS)