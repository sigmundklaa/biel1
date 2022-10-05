
import time
import functools
import numpy as np

NUM_DEC = 5

def f(x):
    return np.exp(x) + x - 3

def df(x):
    return np.exp(x) + 1

def newton(r, *_):
    return r - (f(r)/df(r))

def reduced():
    return round(functools.reduce(newton, range(10), 1), NUM_DEC)

def oneliner():
    return round(functools.reduce(
        lambda x, _: x - ((np.exp(x) + x - 3)/(np.exp(x) + 1)),
        range(10), 1),
        NUM_DEC)

def cached():
    arr = [1] * 10

    for i in range(1, len(arr)):
        arr[i] = newton(arr[i-1])

    return round(arr[-1], NUM_DEC)

def time_it(func):
    arr = []
    val = None

    for _ in range(10000):
        start = time.perf_counter_ns()
        val = func()
        arr.append(time.perf_counter_ns() - start)

    return min(arr), sum(arr) / len(arr), max(arr), val

def fmt_time(func):
    def rounded(x):
        return round(x, 5)

    return func.__name__ + ' returned {3} - min: {0}ns, avg: {1}ns, max: {2}ns'.format(*map(rounded, time_it(func)))

print(fmt_time(reduced))
print(fmt_time(cached))
print(fmt_time(oneliner))
