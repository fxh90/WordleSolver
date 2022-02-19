"""
Puzzle generator
"""

import random

import helper

__author__ = "Z Feng"

max_attempts = 6

def random_puzzle(debug: bool =False) -> None:
    """
    Generate a random puzzle from the Wordle dictionary that the user can play.
    :param debug: Debug mode. Default False. If turned True, the user would know the answer initially.
    :return: None
    """
    potential_answers = helper.get_answer_dictionary()
    legal_guesses = helper.get_guess_dictionary()
    answer = potential_answers[random.randint(0, len(potential_answers) - 1)]
    if debug:
        print(answer)
    for attempt in range(max_attempts):
        while True:
            guess = input(f'\nAttempt {attempt + 1} / {max_attempts}. Please enter your guess\n')
            if guess == 'q':
                quit()
            elif not guess in legal_guesses:
                print(guess, 'is not a word!')
            elif len(guess) == 5:
                break
        similarity = helper.compare(guess, answer)
        if similarity == 3 ** 5 - 1:
            print('Correct! Congratulations!')
            exit()
        pattern = helper.similarity_to_pattern(similarity)
        print('The pattern is', pattern)
    print('Gave over! The answer is', answer)


if __name__ == "__main__":
    random_puzzle()

# EOF
