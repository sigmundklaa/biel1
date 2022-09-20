
from functools import reduce

def nbin(n):
    return '{0:08b}'.format(n)

def o4c(char):
    code = ord(char)
    ncode = code
    
    bitc = reduce(lambda x, y: x + ((code >> y) & 1), range(0, 8), 0)

    if bitc & 1 == 0:
        ncode |= 1 << 7

    return char, nbin(code), nbin(ncode), hex(ncode)

if __name__ == '__main__':
    import sys

    for x in sys.argv[1]:
        print(o4c(x))