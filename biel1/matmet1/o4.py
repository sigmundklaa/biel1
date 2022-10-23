
import tkinter
import numpy as np
import matplotlib
import matplotlib.pyplot as pyplot

matplotlib.use('TkAgg')

def o_1():
    def f(x):
        return np.exp(1-x**2)

    def df(x):
        return -2 * x * f(x)

    def tang(x):
        return -2 * (x - 1) + f(1)

    xvals = np.arange(-2, 2, 0.1)

    pyplot.plot(xvals, f(xvals))
    pyplot.plot(xvals, tang(xvals))
    pyplot.show()

    print(f(1) + df(1) * 0.1)

def o_2():
    def f(x):
        return x ** 2 * (np.sin(x) * np.cos(x) + 1)

    xvals = np.arange(0, 10, 0.1)
    pyplot.plot(xvals, f(xvals))
    pyplot.show()

if __name__ == '__main__':
    o_2()

