import time
import argparse

from threading import Thread
from fib_sample import fib


def fib_threading(loop_num):
    threads = [Thread(target=fib, args=(500000 + i, )) for i in range(loop_num)]

    start = time.time()

    for p in threads:
        p.start()

    for p in threads:
        p.join()

    end = time.time()
    print(f"{end - start} sec.")


if __name__ == '__main__':
    """
    python testing_threading.py --loop_num=20
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--loop_num', help='count loops', type=int)
    args = parser.parse_args()
    loop_num = args.loop_num
    fib_threading(loop_num)
