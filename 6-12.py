from multiprocessing import Process, Value


def increment_value(shared_int):
    shared_int.get_lock().acquire()
    shared_int.value = shared_int.value + 1
    shared_int.get_lock().release()


def increment_value_with_lock(shared_int):
    with shared_int.get_lock():
        shared_int.value = shared_int.value + 1


if __name__ == "__main__":
    integer = Value("i", 0)
    procs = [Process(target=increment_value, args=(integer,)) for _ in range(2)]
    [p.start() for p in procs]
    [p.join() for p in procs]

    print(integer.value)

    procs = [
        Process(target=increment_value_with_lock, args=(integer,)) for _ in range(2)
    ]
    [p.start() for p in procs]
    [p.join() for p in procs]
    print(integer.value)
