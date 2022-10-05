
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

def AAAAAAAAAAAAAAAAAAH():
    return round(functools.reduce(
        lambda x, _: x - ((np.exp(x) + x - 3)/(np.exp(x) + 1)),
        range(10), 1),
        NUM_DEC)

def cached():
    arr = [1] * 10

    for i in range(1, len(arr)):
        arr[i] = newton(arr[i-1])

    return round(arr[-1], NUM_DEC)

print(reduced(), cached(), AAAAAAAAAAAAAAAAAAH())