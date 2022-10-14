
import numpy as np

def f(x):
    return np.exp(x) - 3*x

def df(x):
    return np.exp(x) - 3

def newton(x):
    return x - f(x) / df(x)
