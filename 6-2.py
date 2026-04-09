from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool
import time


def worker(num):
    print(f"Worker {num} is running")
    time.sleep(num)
    return num * num


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(worker, i) for i in range(3)]
        for future in futures:
            print(f"Worker result: {future.result()}")
    print("#" * 20)
    with Pool(processes=2) as pool:
        w1 = pool.apply_async(worker, args=(1,))
        w2 = pool.apply_async(worker, args=(2,))
        w3 = pool.apply_async(worker, args=(3,))
        print(f"Worker 1 result: {w1.get()}")
        print(f"Worker 2 result: {w2.get()}")
        print(f"Worker 3 result: {w3.get()}")
