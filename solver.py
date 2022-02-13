"""
Solver for a Wordle puzzle.
"""

import numpy as np

import helper

__author__ = "Z Feng"


def compute_entropy(legal_guesses: list, potential_answers: list) -> list:
    """
    Compute the information entropy (in bits) of every legal guess in the legal_guesses list. Potential answers are given in a
    seperate list with equal probability assumed.
    :param legal_guesses: list of legal guesses
    :param potential_answers: list of potential answers remaining
    :return: list of information entropies for each entory in legal_guesses. Entropy giben in bits.
    """
    progress = 0
    entropies = []
    for guess in legal_guesses:
        progress += 1
        if progress % 100 == 0:
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
    return entropies


def print_results(legal_guesses: list, entropies: list) -> None:
    """
    Print best guesses according to entropies.
    :param legal_guesses: list of legal words that can be guessed.
    :param entropies: list of entropies (in bits) for every legal guess
    :return: None
    """
    guesses = [(legal_guesses[i], entropies[i]) for i in range(len(legal_guesses))]
    # sort by entropy
    guesses_by_entropy = sorted(guesses, key=lambda e: e[1], reverse=True)
    # print
    print('word\tentropy (bits)')
    for i in range(10):
        print(f'{guesses_by_entropy[i][0]}\t{guesses_by_entropy[i][1]:.3f}')


def main():
    legal_guesses = helper.get_guess_dictionary()
    potential_answers = helper.get_answer_dictionary()
    entropies = compute_entropy(legal_guesses, potential_answers)
    print_results(legal_guesses, entropies)

if __name__ == "__main__":
    main()

# EOF
