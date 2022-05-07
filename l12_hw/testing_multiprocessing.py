import time
import argparse

from multiprocessing import Process, cpu_count
from fib_sample import fib


def fib_multiprocessing_parallel(loop_num):
    """
    используются все процессоры
    """
    processes = [Process(target=fib, args=(500000 + i, )) for i in range(loop_num)]
    start = time.time()

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    end = time.time()
    print(f"{end - start} sec.")


def fib_multiprocessing_fixed_processors(n_proc, loop_num):
    """
    количество задействованных процессоров ограничено n_proc
    """
    processes = [Process(target=fib, args=(500000 + i, )) for i in range(loop_num)]
    start = time.time()

    proc_list = []
    for i, p in enumerate(processes):
        proc_list.append(p)
        if (i + 1) % n_proc == 0 or (i + 1) == loop_num:
            for subproc in proc_list:
                subproc.start()
            for subproc in proc_list:
                subproc.join()
            proc_list = []

    end = time.time()
    print(f"{end - start} sec.")


if __name__ == '__main__':
    """
    python testing_multiprocessing.py --proc=4 --loop_num=20
    """
    cpu_choice_list = list(range(1, int(cpu_count()/2) + 1))
    parser = argparse.ArgumentParser()
    parser.add_argument('--proc', help='processors number', type=int, choices=cpu_choice_list)
    parser.add_argument('--loop_num', help='count loops', type=int)
    args = parser.parse_args()
    n_proc = args.proc
    loop_num = args.loop_num
    fib_multiprocessing_parallel(loop_num)
    fib_multiprocessing_fixed_processors(n_proc, loop_num)
