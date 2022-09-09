
from functools import reduce


def o_2_(pass_):
    print('{} alpha, {} numeric, {} symbols'.format(*reduce(
        lambda tu, char: (tu[0] + char.isalpha(),
                          tu[1] + char.isnumeric(),
                          tu[2] + (not (char.isalpha() or char.isnumeric()))
                          ), pass_, (0, 0, 0))))


def o_2(pass_):
    alph = 0
    dig = 0
    sym = 0

    for c in pass_:
        isalph, isdig = c.isalpha(), c.isnumeric()
        alph += isalph
        dig += isdig
        sym += not (isalph or isdig)

    print(f'{alph} alpha characters, {dig} numeric charcters and {sym} symbols')


def o_3_():
    pass_ = ''

    while len(pass_ := input('Enter password: ')) < 1 or not all(map(lambda x: x < 0, reduce(
        lambda tu, char: (tu[0] - char.isalpha(),
                          tu[1] - char.isnumeric(),
                          tu[2] -
                          (not (char.isalpha() or char.isnumeric()))
                          ), pass_, (2, 2, 0)))):
        print(''.join(('Invalid password, must have more than 2 ',
                       'alpha characters, 2 numeric characters ',
                       'and 1 symbol')))

    print(f'{pass_} is a valid password')


def o_3():
    while 1:
        pass_ = input('Enter password: ')

        alph = 0
        dig = 0
        sym = 0

        for c in pass_:
            isalph, isdig = c.isalpha(), c.isnumeric()
            alph += isalph
            dig += isdig
            sym += not (isalph or isdig)

        if alph < 3 or dig < 3 or sym < 1:
            print(''.join(('Invalid password, must have more than 2 ',
                           'alpha characters, 2 numeric characters ',
                           'and 1 symbol')))
        else:
            print(f'{pass_} is a valid password')
            break


if __name__ == '__main__':
    #o_2_(input('Enter password for check: '))
    o_3_()
