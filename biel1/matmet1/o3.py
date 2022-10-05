
import numpy as np

def f(x):
    return np.exp(x) + x - 3

def df(x):
    return np.exp(x) + 1

def newton(r):
    return r - (f(r)/df(r))

arr = [1] * 10

for i in range(1, len(arr)):
    arr[i] = newton(arr[i-1])

print(arr[-1])