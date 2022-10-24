
import tkinter
import functools
import numpy as np
import math
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

    xvals = np.arange(-10, 10, 0.1)
    pyplot.plot(xvals, f(xvals))
    pyplot.show()

def o_5():
    def integ(x):
        return (1/(math.cos(x)*math.sin(x)) + x)

    return (integ(np.pi/4) - integ(0))

def o_7():
    pass

def o_8():
    def f(x):
        return np.sqrt(x) * np.cos(x)

    def simpson(a, b, n):
        dx = (b - a) / n
        #print(dx, a, b)
        #print(list('{} {}'.format(4 if idx & 1 == 0 else 2, x)
        #        for idx, x in enumerate(np.arange(a+dx, b, dx))))

        return (dx/3) * (
            f(a)
            + sum(4 * f(x) if idx & 1 == 0 else 2 * f(x)
                for idx, x in enumerate(np.arange(a+dx, b, dx)))
            + f(b)
        )

    #print(np.arange(0, 1, 0.1))
    print(simpson(0, 1, 10))

if __name__ == '__main__':
    o_2()

