import time
import requests
from concurrent.futures import ThreadPoolExecutor


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


if __name__ == "__main__":
    start = time.time()
    with ThreadPoolExecutor() as pool:
        urls = [
            "https://www.baidu.com",
            "https://www.cctv.com",
            "https://www.163.com",
            "https://www.sina.com",
            "https://www.bing.com",
        ]
        results = list(pool.map(get_status_code, urls))
        for result in results:
            print(result)
    end = time.time()
    print(f"Execution time: {end - start:.2f} seconds")
