# import time
# import asyncio


# def sync_task(task_id: int, delay: int) -> str:
#     print(f"[SYNC] Task {task_id} boshlandi")
#     time.sleep(delay)
#     print(f"[SYNC] Task {task_id} tugadi ({delay}s)")
#     return f"Task {task_id} natija"


# async def async_task(task_id: int, delay: int) -> str:
#     print(f"[ASYNC] Task {task_id} boshlandi")
#     await asyncio.sleep(delay)
#     print(f"[ASYNC] Task {task_id} tugadi ({delay}s)")
#     return f"Task {task_id} natija"

# def run_sync():
#     print("\n" + "=" * 50)
#     print("SYNC DEMO")
#     print("=" * 50)

#     start = time.perf_counter()

#     results = []
#     results.append(sync_task(1, 2))
#     results.append(sync_task(2, 2))
#     results.append(sync_task(3, 2))

#     elapsed = time.perf_counter() - start
#     print(f"\n[SYNC] Natijalar: {results}")
#     print(f"[SYNC] Umumiy vaqt: {elapsed:.2f} sekund")


# async def run_async():
#     print("\n" + "=" * 50)
#     print("ASYNC DEMO")
#     print("=" * 50)

#     start = time.perf_counter()

#     results = await asyncio.gather(
#         async_task(1, 2),
#         async_task(2, 2),
#         async_task(3, 2),
#     )

#     elapsed = time.perf_counter() - start
#     print(f"\n[ASYNC] Natijalar: {results}")
#     print(f"[ASYNC] Umumiy vaqt: {elapsed:.2f} sekund")


# if __name__ == "__main__":
#     run_sync()
#     asyncio.run(run_async())


import asyncio

async def hisobla(son):
    print(f"{son} ning kvadrati hisoblanmoqda...")
    await asyncio.sleep(3)
    print(f"{son} kvadrati = {son**2}")



async def test():
    print(f"Test ishga tushdi")
    await asyncio.sleep(1)
    print(f"Test tugadi")


async def test2():
    print(f"Test2 ishga tushdi")
    await asyncio.sleep(0)
    print(f"Test2 tugadi")

async def main():
    # 3 ta vazifani parallel bajarish
    await asyncio.gather(
        hisobla(2),
        test(),
        test2()
    )

asyncio.run(main())