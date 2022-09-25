import numpy as np

def cramer(a, b, i):
    subbed = a.copy()
    subbed[:,i-1] = b

    return (
        np.linalg.det(subbed),
        np.linalg.det(subbed) / np.linalg.det(a),
    )

def main():
    A_orig = np.array([
        [x**(4 - y) for y in range(0, 5)] for x in range(1, 6)
    ])
    print(A_orig)

    print(cramer(A_orig.copy(), np.array([0, 0, 1, 3, 0]), 2))

if __name__ == '__main__':
    main()
