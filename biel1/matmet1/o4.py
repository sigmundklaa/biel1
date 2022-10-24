
import tkinter
import functools
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as pyplot

matplotlib.use('TkAgg')

def o_1():
    def f(x):
        return 2 * np.exp(1-x**2)

    def df(x):
        return -2 * x * f(x)

    def tang(x):
        return df(1) * (x - 1) + f(1)

    xvals = np.arange(-2, 2, 0.1)

    pyplot.plot(xvals, f(xvals))
    pyplot.plot(xvals, tang(xvals))
    pyplot.show()

    print(f(1) + df(1) * 0.1)
    print(f(1.1))

def o_2():
    def f(x):
        return x ** 2 * (np.sin(x) * np.cos(x) + 1)

    xvals = np.arange(-3, 3, 0.1)
    pyplot.plot(xvals, f(xvals))
    pyplot.show()

def o_3():
    def f(x):
        return ((x ** 2) * np.sin(x)) + (2 * x * np.cos(x)) + (2 * np.sin(x)) + ((1/3) * (x ** 3))

    print(f(3) - f(-3))

def o_5():
    def integ(x):
        return (-1/(math.cos(x)) + x)

    print(integ(np.pi/4) - integ(0))

def o_7():
    def f(x):
        return np.sqrt(x + x**3)

    def rkm(f, start, stop, n):
        dx = (stop - start) / n
        return sum(f(x + dx/2)*dx for x in np.arange(start, stop, dx))

    print(round(rkm(f, 0, 1, 10), 6))

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
    print(round(simpson(0, 1, 10), 8))

if __name__ == '__main__':
    o_8()

