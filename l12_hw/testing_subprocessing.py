import time
import argparse
import subprocess
from os import cpu_count


def fib_processes_parallel(n_proc, loop_num):
    """
    количество задействованных процессоров ограничено n_proc
    """
    start = time.time()

    proc_list = []
    for i in range(loop_num):
        proc = subprocess.Popen(['python', r"fib_sample.py", str(500000 + i)])
        proc_list.append(proc)
        # "пачки по количеству задействованных процессоров n_proc"
        if (i + 1) % n_proc == 0 or (i + 1) == loop_num:
            for subproc in proc_list:
                subproc.wait()
            proc_list = []

    end = time.time()
    print(f"{end - start} sec.")


def fib_processes_sequence(loop_num):
    """
    Последовательное выполнение
    """
    start = time.time()

    for i in range(loop_num):
        proc = subprocess.Popen(['python', r"fib_sample.py", str(500000 + i)])
        proc.wait()

    end = time.time()
    print(f"{end - start} sec.")


if __name__ == '__main__':
    """
    python testing_subprocessing.py --proc=4 --loop_num=20
    """
    cpu_choice_list = list(range(1, int(cpu_count()/2) + 1))
    parser = argparse.ArgumentParser()
    parser.add_argument('--proc', help='count subprocesses start', type=int, choices=cpu_choice_list)
    parser.add_argument('--loop_num', help='count loops', type=int)
    args = parser.parse_args()
    n_proc = args.proc
    loop_num = args.loop_num
    fib_processes_sequence(loop_num)
    fib_processes_parallel(n_proc, loop_num)
