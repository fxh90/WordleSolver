"""
Solver for a Wordle puzzle.
"""

import os
import warnings
import numpy as np

import helper

__author__ = "Z Feng"

max_attempts = 5
warnings.filterwarnings('ignore')

def compute_entropy(legal_guesses: list, potential_answers: list, do_print: bool = True) -> np.ndarray:
    """
    Compute the information entropy (in bits) of every legal guess in the legal_guesses list. Potential answers are
    given in a separate list with equal probability assumed.
    :param legal_guesses: list of legal guesses
    :param potential_answers: list of potential answers remaining
    :return: list of information entropies for each entry in legal_guesses. Entropy given in bits.
    """
    progress = 0
    entropies = []
    for guess in legal_guesses:
        progress += 1
        if do_print:
            if progress % 500 == 0:
                print(f'{progress}/{len(legal_guesses)}: {guess}')
        similarity_counts = np.zeros(3 ** 5, dtype=float)
        for target in potential_answers:
            similarity = helper.compare(guess, target)
            similarity_counts[similarity] += 1
        p = similarity_counts / len(potential_answers)
        entropy_contributions = - p * np.log2(p)
        entropy_contributions[np.isnan(entropy_contributions)] = 0
        entropy = np.sum(entropy_contributions)
        entropies.append(entropy)
    return np.array(entropies)


def compute_probabilities(legal_guesses: list, potential_answers: list) -> np.ndarray:
    """
    Compute the possibility of every legal guess in the legal_guesses list. Potential answers are given in a separate
    list with equal probabilities assumed.
    :param legal_guesses: list of legal guesses
    :param potential_answers: list of potential answers
    :return: list of probabilities for each entry in legal_guesses.
    """
    p = 1 / len(potential_answers)
    probabilities = [(word in potential_answers) * p for word in legal_guesses]
    return np.array(probabilities)


def compute_score_1(entropies: np.ndarray, probabilities: np.ndarray) -> np.ndarray:
    """
    First version of computing a score combining entropy and probability to make (hopefully) better choices when making
    a guess.
    The proposed function of score is: S = (H + p) / (1.1 ^ 2 - p ^2)
    :param entropies: entropy (H)
    :param probabilities: probability (p)
    :return: score (S)
    """
    scores = (entropies + probabilities) / (1.1 ** 2 - probabilities ** 2)
    return scores


def print_results(legal_guesses: list, entropies: np.ndarray, probabilities: np.ndarray,
                  scores: np.ndarray, lines: int = 5) -> None:
    """
    Print best guesses according to entropies.
    :param legal_guesses: list of legal words that can be guessed.
    :param entropies: list of entropies (in bits) for every legal guess
    :param lines: number of lines printed
    :return: None
    """
    guesses = [(legal_guesses[i], entropies[i], probabilities[i], scores[i]) for i in range(len(legal_guesses))]
    # sort by entropy
    guesses_by_entropy = sorted(guesses, key=lambda e: e[1], reverse=True)
    # sort by probability
    guesses_by_probability = sorted(guesses, key=lambda e: e[2], reverse=True)
    # sort by score
    guesses_by_score = sorted(guesses, key=lambda e: e[3], reverse=True)
    # print
    print('word\tentropy (bits)\tword\tprobability\t\tword\tscore')
    for i in range(lines):
        print(f'{guesses_by_entropy[i][0]}\t{guesses_by_entropy[i][1]:.3f}'
              + f'\t\t\t{guesses_by_probability[i][0]}\t{guesses_by_probability[i][2]:.3e}'
              + f'\t\t{guesses_by_score[i][0]}\t{guesses_by_score[i][3]:3e}')


def refine_potential_answers(guess: str, potential_answers: list, similarity: int) -> list:
    """
    Refine potential answers from the result of a particular guess.
    :param guess: guessed word
    :param potential_answers: potential answers to refine from
    :param similarity: similarity between guess and true answer
    :return: list of refined potential answers
    """
    refined_answers = []
    for target in potential_answers:
        if helper.compare(guess, target) == similarity:
            refined_answers.append(target)
    return refined_answers


def accept_test_result():
    """
    Let the user input the word guessed and the result as a pattern.
    :return: guess, pattern
    """
    while True:
        usr_input = input('Please enter the word attempted and pattern received\n')
        if usr_input == 'q':
            print('Solver exited!')
            quit()
        splits = usr_input.split()
        if len(splits) == 2:
            if len(splits[0]) == len(splits[1]) and all([letter in ('0', '1', '2') for letter in splits[1]]):
                break
        print('Unrecognisable input. Please try again.')
    return splits[0], splits[1]


def man_solver():
    """
    Manual solver of a Wordle puzzle.
    """
    legal_guesses = helper.get_guess_dictionary()
    potential_answers = helper.get_answer_dictionary()
    for attempt in range(max_attempts):
        if attempt == 0:
            # initial entropies
            if os.path.exists('initial_entropies.npy'):
                print('loading initial_entropies.npy...')
                with open('initial_entropies.npy', 'rb') as npy_file:
                    entropies = np.load(npy_file)
            else:
                entropies = compute_entropy(legal_guesses, potential_answers)
                print('saving initial_entropies.npy...')
                with open('initial_entropies.npy', 'wb') as npy_file:
                    np.save(npy_file, entropies)
            # initial probabilities
            if os.path.exists('initial_probabilities.npy'):
                print('loading initial_probabilities.npy...')
                with open('initial_probabilities.npy', 'rb') as npy_file:
                    probabilities = np.load(npy_file)
            else:
                probabilities = compute_probabilities(legal_guesses, potential_answers)
                print('saving initial_probabilities.npy...')
                with open('initial_probabilities.npy', 'wb') as npy_file:
                    np.save(npy_file, probabilities)
        else:
            entropies = compute_entropy(legal_guesses, potential_answers)
            probabilities = compute_probabilities(legal_guesses, potential_answers)
        scores = compute_score_1(entropies, probabilities)
        print_results(legal_guesses, entropies, probabilities, scores)
        guess, pattern = accept_test_result()
        similarity = helper.pattern_to_similarity(pattern)
        if similarity == 3 ** 5 - 1:
            print('Congratulations!')
            break
        potential_answers = refine_potential_answers(guess, potential_answers, similarity)


def auto_solver(strategy: str = 'entropy first'):
    """
    Generator object that solves a Wordle puzzle automatically according to a given strategy.
    :param strategy: 'entropy first', 'score 1'
    """
    legal_guesses = helper.get_guess_dictionary()
    potential_answers = helper.get_answer_dictionary()
    first_attempt = True
    while True:
        if first_attempt:
            # initial entropies
            if os.path.exists('initial_entropies.npy'):
                with open('initial_entropies.npy', 'rb') as npy_file:
                    entropies = np.load(npy_file)
            else:
                entropies = compute_entropy(legal_guesses, potential_answers, do_print=False)
                with open('initial_entropies.npy', 'wb') as npy_file:
                    np.save(npy_file, entropies)
            if not strategy == 'entropy first':
                # initial probabilities
                if os.path.exists('initial_probabilities.npy'):
                    with open('initial_probabilities.npy', 'rb') as npy_file:
                        probabilities = np.load(npy_file)
                else:
                    probabilities = compute_probabilities(legal_guesses, potential_answers)
                    with open('initial_probabilities.npy', 'wb') as npy_file:
                        np.save(npy_file, probabilities)
            first_attempt = False
        else:
            entropies = compute_entropy(legal_guesses, potential_answers, do_print=False)
            if not strategy == 'entropy first':
                probabilities = compute_probabilities(legal_guesses, potential_answers)
        if strategy == 'entropy first':
            if len(potential_answers) == 1:
                guess = potential_answers[0]
            else:
                guesses = [(legal_guesses[i], entropies[i]) for i in range(len(legal_guesses))]
                guess = sorted(guesses, key=lambda e: e[1], reverse=True)[0][0]
        elif strategy == 'score 1':
            scores = compute_score_1(entropies, probabilities)
            guesses = [(legal_guesses[i], scores[i]) for i in range(len(legal_guesses))]
            guess = sorted(guesses, key=lambda e: e[1], reverse=True)[0][0]
        else:
            raise NotImplementedError
        yield guess
        similarity = yield
        potential_answers = refine_potential_answers(guess, potential_answers, similarity)


if __name__ == "__main__":
    man_solver()


# EOF
