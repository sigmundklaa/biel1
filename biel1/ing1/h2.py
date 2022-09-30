def draw_figure(num_wrong_guesses):
    print([
        '  +---+\n'
        '  |   |\n'
        '      |\n'
        '      |\n'
        '      |\n'
        '      |\n'
        '=========',
        '  +---+\n'
        '  |   |\n'
        '  O   |\n'
        '      |\n'
        '      |\n'
        '      |\n'
        '=========',
        '  +---+\n'
        '  |   |\n'
        '  O   |\n'
        '  |   |\n'
        '      |\n'
        '      |\n'
        '=========',
        '  +---+\n'
        '  |   |\n'
        '  O   |\n'
        ' /|   |\n'
        '      |\n'
        '      |\n'
        '=========',
        '  +---+\n'
        '  |   |\n'
        '  O   |\n'
        ' /|\  |\n'
        '      |\n'
        '      |\n'
        '=========',
        '  +---+\n'
        '  |   |\n'
        '  O   |\n'
        ' /|\  |\n'
        ' /    |\n'
        '      |\n'
        '=========',
        '  +---+\n'
        '  |   |\n'
        '  O   |\n'
        ' /|\  |\n'
        ' / \  |\n'
        '      |\n'
        '========='
    ][num_wrong_guesses])

def request_word_from_user():
    return input('Enter word: ').lower().strip()

def request_letter_from_user():
    letter = input('Enter letter: ').lower().strip()

    return len(letter) == 1, letter

def make_needed_letters_list(word):
    return set(word)

def create_word_outline(word, guessed):
    return ''.join(x if x in guessed else '_' for x in word)

def hangman():
    print('Welcome to hangman!')
    word = request_word_from_user()
    letters = make_needed_letters_list(word)
    guessed = set()
    correct = set()
    lives = 6

    while True:
        print(','.join(guessed))
        print(f'Lives left: {lives}')
        draw_figure(6 - lives)
        print(create_word_outline(word, guessed))

        ok, let = request_letter_from_user()

        if not ok:
            print(f'Invalid letter {let}')
            continue

        if let in guessed:
            print(f'Already guessed {let}')
            continue

        guessed.add(let)

        if let in letters:
            correct.add(let)
            print('Letter is in word')
        else:
            lives -= 1
            print('Letter is not in word')

        if len(correct) == len(letters):
            print('You won')
            return

        if lives <= 0:
            print('You lost')
            print(f'The word was: {word}')
            return

def main():
    try:
        while 1:
            hangman()
            print('Restarting...')
    except KeyboardInterrupt:
        print('Hangman exited')
        return

if __name__ == '__main__':
    main()