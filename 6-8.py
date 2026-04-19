import asyncio
import concurrent.futures
import functools
import time
from typing import Dict, Generator, List


def partition(data: List, chunk_size: int) -> Generator[List]:
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


def map_frequenceies(chunk: List[str]) -> Dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split("\t")
        if counter.get(word):
            counter[word] = counter[word] + int(count)
        else:
            counter[word] = int(count)
    return counter


def merge_dictionaries(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second.keys():
        if key in merged.keys():
            merged[key] = merged[key] + second[key]
        else:
            merged[key] = second[key]
    return merged


async def main(partition_size: int):
    with open(
        "./data/googlebooks-eng-all-1gram-20120701-a", "r", encoding="utf-8"
    ) as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor() as pool:
            for chunk in partition(contents, partition_size):
                tasks.append(
                    loop.run_in_executor(
                        pool, functools.partial(map_frequenceies, chunk)
                    )
                )
            intermediate_results = await asyncio.gather(*tasks)
            final_result = functools.reduce(merge_dictionaries, intermediate_results)
            print(f"Aardvark has appeared {final_result['Aardvark']} time.")
            end = time.time()
            print(f"MapReduce took: {end-start:.4f} seconds.")


if __name__ == "__main__":
    asyncio.run(main(partition_size=60000))
