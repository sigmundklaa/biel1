
from operator import (
    __add__,
    __sub__,
    __mul__
)


def o_1(*args):
    funcs = {
        'sum': lambda *args: sum(args),
        'difference': lambda *args: __sub__(*reversed(args)),
        'product': __mul__,
        'average': lambda *args: sum(args) / len(args),
        'distance': lambda *args: abs(__sub__(*args)),
        'maximum': max,
        'minimum': min
    }

   # for k, v in funcs.items():
    #print(f'{k[0].upper()}{k[1:]}: {v(*args)}')

    print(''.join(f'{k[0].upper()}{k[1:]}: {v(*args)}')
          for k, v in funcs.items())


def o_3(tank, eff, price):
    milageleft = tank * eff
    costper = (100 / eff) * price

    print(f'Cost per 100km: {costper}, km left: {milageleft}')


def o_4(num):
    if not (0 < num < 1e6):
        print('Invalid number')
    elif num < 1e3:
        print('No seperator, number < 1000')
    else:
        nstr = str(num)
        idx = len(nstr) - 3
        nstr = nstr[:idx] + ',' + nstr[idx:]
        print(nstr)


def o_6(num):
    print(' '.join(reversed(str(num))))


def o_7(year):
    a = year % 19
    b, c = year // 100, year % 100
    d, e = b // 4, b % 4
    g = (8 * b + 13) // 25
    h = (19 * a + b - d - g + 15) % 30
    j, k = c // 4, c % 4
    m = (a + 11 * h) // 319
    r = (2 * e + 2 * j - k - h + m + 32) % 7
    n = (h - m + r + 90) // 25
    p = (h - m + r + n + 19) % 32

    #print(p, n)
    months = ["januar", "februar", "mars", "april", "mai", "juni",
              "juli", "august", "september", "oktober", "november", "desember"]

    print(f'{p}. {months[n-1]}')


if __name__ == '__main__':
    o_1(*[(int(input(f'Input number {i+1}: '))) for i in range(2)])
    o_3(20, 0.8, 1)
    o_4(999)
    o_4(5000)
    o_4(670000)
    o_6(123456)
    o_7(2001)

#tall = '12345'
#medkomma = tall[:2] + ',' + tall[2:]
