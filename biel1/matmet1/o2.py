
import math
import numpy as np

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def printe(cls, string):
        return print(string + cls.ENDC)

def cbroot(x):
    return x ** (1/3)

def f_d(x, h):
    def f(x):
        return cbroot(1+math.e**(x**2))

    return (f(x + h) - f(x)) / h

def cramer(a, b, i):
    subbed = a.copy()
    subbed[:,i-1] = b

    return (
        np.linalg.det(subbed),
        np.linalg.det(subbed) / np.linalg.det(a),
    )

def main():
    bcolors.printe(bcolors.OKGREEN + f'Question 8: {f_d(1,1e-8)}')

    A_orig = np.array([
        [x**(4 - y) for y in range(0, 5)] for x in range(1, 6)
    ])

    bcolors.printe(bcolors.OKCYAN + f'Question 3: ')
    print(A_orig)

    bcolors.printe(bcolors.OKGREEN + ', '.join(map(str, cramer(A_orig.copy(), np.array([0, 0, 1, 3, 0]), 2))))

if __name__ == '__main__':
    main()
