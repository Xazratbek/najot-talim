import time
import threading
import urllib.request
import json

URLS = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
    "https://jsonplaceholder.typicode.com/posts/4",
    "https://jsonplaceholder.typicode.com/posts/5",
]


def fetch_post(url: str) -> dict:
    start = time.perf_counter()
    thread_name = threading.current_thread().name

    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    elapsed = time.perf_counter() - start
    print(
        f"[{thread_name}] fetched {url} | post_id={data['id']} | "
        f"title={data['title'][:30]!r} | took={elapsed:.3f}s"
    )
    return data


def run_single_thread():
    print("\n=== SINGLE THREAD (ketma-ket) ===")
    start = time.perf_counter()

    results = []
    for url in URLS:
        results.append(fetch_post(url))

    elapsed = time.perf_counter() - start
    print(f"SINGLE THREAD total time: {elapsed:.3f}s")
    return results


def worker(url: str, results: list, index: int):
    try:
        results[index] = fetch_post(url)
    except Exception as e:
        results[index] = {"error": str(e), "url": url}
        print(f"[{threading.current_thread().name}] ERROR: {url} -> {e}")


def run_multi_thread():
    print("\n=== MULTITHREADING (bir nechta thread) ===")
    start = time.perf_counter()

    threads = []
    results = [None] * len(URLS)

    for i, url in enumerate(URLS):
        t = threading.Thread(target=worker, args=(url, results, i), name=f"Thread-{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.perf_counter() - start
    print(f"MULTITHREADING total time: {elapsed:.3f}s")
    return results


if __name__ == "__main__":
    run_single_thread()
    run_multi_thread()