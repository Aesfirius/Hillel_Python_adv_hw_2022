import sys


def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    print("n = {0}, result % 100 = {1}".format(n, a % 100))


if __name__ == "__main__":
    num = int(sys.argv[1])
    fib(num)
