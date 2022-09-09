
def t_1(*args):
    print(min(int(input(f'Enter value {x+1}: ')) for x in range(3)))


if __name__ == '__main__':
    import sys

    try:
        fn = sys.argv[1]
    except IndexError:
        print('Missing argument 1')
    else:

        if not fn.startswith('t_') or fn not in globals():
            print('Invalid function')
        else:
            globals()[fn](*sys.argv[2:])
