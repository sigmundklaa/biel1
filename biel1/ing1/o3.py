
import sys
import functools

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

def print_factory():
    def _print_sub(*args):
        _print_sub.count += 1
        nargs = list(args) + ['\n']

        return print(bcolors.OKGREEN + '\t' + chr(ord('a') + _print_sub.count - 1) + ')', *nargs, end=bcolors.ENDC)

    _print_sub.count = 0

    return _print_sub

def question(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        print(f'{bcolors.OKCYAN} Oppgave {func.__name__.split("_")[1]} {bcolors.ENDC}')
        return func(*args, **kwargs)

    func.print_sub = f.print_sub = print_factory()

    return f

def o_1():
    person = {
        'navn': 'Steinar',
        'alder': 27,
        'favorittfarger': ['oransje', 'brun', 'sort'],
    }

    o_1.print_sub(f'{person["navn"]} er {person["alder"]} år')

    try:
        person['key']
    except Exception as e:
        o_1.print_sub(f'person["key"] gir {type(e).__name__}, person.get("key") returnerer {person.get("key")} siden det er default verdien til get sitt andre parameter')

    o_1.print_sub(f'{person["navn"]} er {person["alder"]} og liker {", ".join(person["favorittfarger"][:-1])} og {person["favorittfarger"][-1]}.')

def o_2():
    o_2.print_sub('iii. x = (25,50) er en tuple')
    o_2.print_sub('i. ikke mulig å endre etter definisjon')
    o_2.print_sub('en tuple er indeksert')

def o_3():
    def func(*input_list):
        return [x for x in input_list if 15 < x < 35]

    for _ in range(5):
        o_3.print_sub()

    o_3.print_sub(func(*[5, 12, 7, 53, 88, 21, 34, 73, 0, 432]))

def o_4():
    def calc_series(*resistors):
        return sum(resistors)

    def calc_para(*resistors):
        return 1 / functools.reduce(lambda x, y: x + 1 / y, resistors, 0)

    list_ = [220, 1000, 100, 220, 560]

    o_4.print_sub(calc_series(*list_))
    o_4.print_sub(calc_para(*list_))

def o_5():
    def f(x):
        def g(n):
            return (2*n - 1) / n

        return sum(map(g, range(1, x + 1)))

    o_5.print_sub(f(10))    

def o_6():
    def f(x):
        def _get_input(*args, **kwargs):
            inp = input(*args, **kwargs)
            #print("\r", end="")
            #sys.stdout.flush()

            return inp

        person_str = f' person {x}: '

        return {
            'navn': _get_input('Navn' + person_str),
            'alder': int(_get_input('Alder' + person_str))
        }

    o_6.print_sub(f(1))
    o_6.print_sub(functools.reduce(lambda x, y: {**x, **{y: f(y+1)}}, range(5), {}))

if __name__ == '__main__':
    locs = locals().copy()
    for k, v in locs.items():
        if k.startswith('o_'):
            question(v)()
