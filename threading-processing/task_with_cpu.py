import time
import threading
import multiprocessing


def cpu_task(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total


def thread_worker(n: int) -> None:
    cpu_task(n)


def process_worker(n: int) -> None:
    cpu_task(n)


def run_threads(n: int, workers: int) -> None:
    print("\n=== CPU TASK WITH THREADS ===")
    start = time.perf_counter()
    threads = []

    for i in range(workers):
        t = threading.Thread(target=thread_worker, args=(n,), name=f"Thread-{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.perf_counter() - start
    print(f"Threads total time: {elapsed:.3f}s")


def run_processes(n: int, workers: int) -> None:
    print("\n=== CPU TASK WITH PROCESSES ===")
    start = time.perf_counter()
    processes = []

    for _ in range(workers):
        p = multiprocessing.Process(target=process_worker, args=(n,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    elapsed = time.perf_counter() - start
    print(f"Processes total time: {elapsed:.3f}s")


if __name__ == "__main__":
    N = 20_000_000
    WORKERS = 4

    run_threads(N, WORKERS)
    run_processes(N, WORKERS)