"""
Solver for a Quordle puzzle
https://www.quordle.com/#/
"""

import os
import pickle
import numpy as np

import helper
import solver

__author__ = "Z Feng"

max_attempts = 9


def accept_quordle_test_result():
    """
    Let the user input the word guessed and the results as 4 matching patterns
    :return: guess, pattern
    """
    while True:
        usr_input = input('Please enter the word attempted and patterns received\n')
        if usr_input == 'q':
            print('Solver exited!')
            quit()
        splits = usr_input.split()
        if len(splits) == 5:
            exit_flag = all([len(splits[0]) == len(splits[i + 1])
                             and all([letter in ('0', '1', '2') for letter in splits[i + 1]])
                             for i in range(4)])
            if exit_flag:
                break
        print('Unrecognisable input. Please try again.')
    return splits[0], (splits[1], splits[2], splits[3], splits[4])


def man_solver():
    """
    Manual solver of a Quordle puzzle
    """
    legal_guesses = helper.get_guess_dictionary()
    potential_answers = [helper.get_answer_dictionary() for i in range(4)]
    solved_puzzles = [False for i in range(4)]
    for attempt in range(max_attempts):
        if attempt == 0:
            entropies = initial_entropies
            probabilities = initial_probabilities
            scores = solver.compute_score_1(entropies, probabilities)
            total_entropies = entropies * 4
            total_probabilities = probabilities * 4
        else:
            total_entropies = np.zeros(len(legal_guesses))
            total_probabilities = np.zeros(len(legal_guesses))
            scores = np.zeros(len(legal_guesses))
            for puzzle_num in range(4):
                if not solved_puzzles[puzzle_num]:
                    entropies = solver.compute_entropy(legal_guesses, potential_answers[puzzle_num])
                    probabilities = solver.compute_probabilities(legal_guesses,
                                                                  potential_answers[puzzle_num])
                    total_entropies += entropies
                    total_probabilities += probabilities
                    scores += solver.compute_score_1(entropies, probabilities)
            scores /= (4 - sum(solved_puzzles))
        solver.print_results(legal_guesses, total_entropies, total_probabilities, scores)
        guess, patterns = accept_quordle_test_result()
        for puzzle_num in range(4):
            if not solved_puzzles[puzzle_num]:
                similarity = helper.pattern_to_similarity(patterns[puzzle_num])
                if similarity == 3 ** 5 - 1:
                    solved_puzzles[puzzle_num] = True
                else:
                    potential_answers[puzzle_num] = solver.refine_potential_answers(
                        guess, potential_answers[puzzle_num], similarity)
        if all(solved_puzzles):
            print('Congratulations!')
            break


# initialise similarity LUT
if os.path.exists('similarity_lut.pkl'):
    with open('similarity_lut.pkl', 'rb') as pkl_file:
        similarity_lut = pickle.load(pkl_file)
else:
    print('Initialising similarity LUT...')
    similarity_lut = helper.gen_similarity_LUT()
    with open('similarity_lut.pkl', 'wb') as pkl_file:
        pickle.dump(similarity_lut, pkl_file)
# initial entropies
if os.path.exists('initial_entropies.npy'):
    print('loading initial_entropies.npy...')
    with open('initial_entropies.npy', 'rb') as npy_file:
        initial_entropies = np.load(npy_file)
else:
    initial_entropies = solver.compute_entropy()
    print('saving initial_entropies.npy...')
    with open('initial_entropies.npy', 'wb') as npy_file:
        np.save(npy_file, initial_entropies)
# initial probabilities
if os.path.exists('initial_probabilities.npy'):
    print('loading initial_probabilities.npy...')
    with open('initial_probabilities.npy', 'rb') as npy_file:
        initial_probabilities = np.load(npy_file)
else:
    initial_probabilities = solver.compute_probabilities()
    print('saving initial_probabilities.npy...')
    with open('initial_probabilities.npy', 'wb') as npy_file:
        np.save(npy_file, initial_probabilities)

if __name__ == "__main__":
    man_solver()

# EOF
