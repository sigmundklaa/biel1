
import random
from functools import reduce


def o_1(string: str):
    print(' '.join(x for x in string))
    print(' '.join(reversed(list(string))))
    print(' '.join(x for idx, x in enumerate(string) if idx & 1 == 0))
    print(' '.join(x for x in string if x in 'ae'))


def o_2(list_: list):
    print(len(list_))
    #  5
    # 88
    list_.extend([18, 346, 254])
    print(len(list_))
    list_.sort()
    list_.reverse()


def o_3(list_: list):
    out = []

    for x in list_:
        print(f'{x} har typen {type(x)}')

        if isinstance(x, int):
            out.append(x)
        elif isinstance(x, float):
            out.append(round(x))

    print(out)


def o_4():
    l = [x for x in range(1, 100) if x % 11 == 0]
    print(l, sum(l))


def o_5():
    for x in range(1, 10):
        print(str(x) * x)


def o_6():
    print(reduce(lambda x, y: x + ((2 * y) - 1) / y, range(1, 10), 0))


def o_7():
    spin = random.randint(0, 37)  # 37 = 00

    if 0 < spin < 37:
        for x in (
            spin,
            'Rød' if spin & 1 else 'Sort',
            'Oddetall' if spin & 1 else 'Partall',
            '1 - 18' if spin < 19 else '19 - 36'
        ):
            print(f'Betal ut for {x}')
    else:
        print(f'Betal ut for {"0" if not spin else "00"}')


if __name__ == '__main__':
    o_1('Hei, jeg er et kjempebra python-skript')
    o_2([5, 12, 7, 53, 88, 21, 34, 73, 0, 432])
    o_3([34, "en streng", 108, 0.53, 'b', True, 7.3, 1])
    o_4()
    o_5()
    o_6()
    o_7()
