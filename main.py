import os
import random
import json


def create_hints():
    hints = dict()
    if number % 2 == 0:
        hints[1] = 'The number is Even.'
    else:
        hints[1] = 'The number is Odd.'

    hints[2] = f'The sum of digits of the number is {sum_of_digits(number)}.'
    if is_prime(number):
        hints[3] = 'The number is Prime.'
    else:
        hints[3] = 'The number is not Prime.'
    return hints


def give_hint():
    percentage = (attempts / max_attempts) * 100
    hint = ''
    if percentage > 20:
        hint = hints[1]
    if percentage > 50:
        hint = hints[2]
    if percentage > 70:
        hint = hints[3]
    return hint


def is_prime(num):
    flag = True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            flag = False
            break
    return flag


def sum_of_digits(num):
    sum_digits = 0
    while num:
        sum_digits += (num % 10)
        num = num // 10
    return sum_digits


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def display_fame():
    clear_screen()
    print("""
      ***************************************
              Leader Board""", end='')
    print(f' ( Level {level} )', end='')
    print("""
      ***************************************
       Rank       Name                 Score
      ---------------------------------------    """)
    data = read_fame()
    for name, scores in data[str(level)]:
        print(f'\t{scores[1]}\t {name.ljust(20)[:20]}   {str(scores[0]).rjust(3)[:3]}')


def get_number(msg_str):

    while True:
        num = input(msg_str)
        if num.isdigit():
            break
    return int(num)


def set_limits(lvl):
    if lvl == 1:
        max_range = 50
        no_attempts = 5
    elif lvl == 2:
        max_range = 100
        no_attempts = 10
    else:
        max_range = 1000
        no_attempts = 20
    return max_range, no_attempts


def instruction():
    print("""\n
    *********************************************************************************************
    \t\t\tWelcome to Number Guess Game!!!
    *********************************************************************************************
    Computer will generate a random number between 
    1 to 50 for Level 1 , 1 to 100 for Level 2 , 1 to 1000 for Level 3.
    
    You have to guess that number.
    If your guess is correct, you WON the game!!!
    if your guess is greater than the correct number, you will get "The guess is too high".
    if your guess is less, then you will get "The guess is too low".
    You guess again.
    """)


def read_fame():

    with open('fame.json') as f:
        hist_fame = json.load(f)
    for lvl in range(1, 4):
        if str(lvl) not in hist_fame:
            hist_fame[str(lvl)] = []
    return hist_fame


def write_fame():
    hist_fame = read_fame()
    hist_fame[str(level)].append([player_name, [score, 0]])
    sorted_data = sorted(hist_fame[str(level)], key=lambda x: x[1], reverse=True)[:10]
    fame = [[player, [scores[0], i+1]] for i, (player, scores) in enumerate(sorted_data)]
    hist_fame[str(level)] = fame
    json_object = json.dumps(hist_fame)

    with open("fame.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == '__main__':
    clear_screen()
    instruction()

    option = input('    Press (Enter) to Start/ Any other key to Exit ? ')
    if option != '':
        exit()

    player_name = input('    Enter your Name : ')

    while True:
        print("    Let's play\n")
        while True:
            level = get_number("    Enter the level 1/2/3 ? ")
            if 0 < level < 4:
                break
        print('    Level - ', level)

        attempts = 0

        high_range, max_attempts = set_limits(level)
        number = random.randint(1, high_range)
        hints = create_hints()
        # print(number)
        print(f'    You have {max_attempts} attempts.')
        while True:
            guess = get_number(f'    Guess a number (1 - {high_range}) : ')
            attempts += 1
            if guess == number:
                print('\n\n\t    Congratulations!!! You guessed the number.')
                if attempts == 1:
                    print(f'\t    You took {attempts} attempt.')
                else:
                    print(f'\t    You took {attempts} attempts.')
                score = int(((max_attempts - attempts + 1) / max_attempts) * 100)
                print(f'\t    Your score is {score}.\n')
                _ = input("")
                write_fame()
                display_fame()
                break
            elif guess > number:
                print('    Your guess is too high.')
            else:
                print('    Your guess is too low.')

            if attempts == max_attempts:
                print('    You have reached maximum number of attempts.')
                print('    You lost the game!!!')
                print(f'    The number is {number}.')
                print('    Better Luck next game.')

                read_fame()
                display_fame()

                break

            if max_attempts-attempts == 1:
                print(f'    You have {max_attempts - attempts} attempt left with.')
            else:
                print(f'    You have {max_attempts-attempts} attempts left with.')

            hint = give_hint()
            if hint != '':
                print(f'    *** Hint : {hint}')

        while True:
            play_again = input('\n    Do you want to Play again (Y/N) ? ').upper()
            if play_again in 'YN':
                break
        if play_again == 'N':
            break
    print('    Thank you!!!')
