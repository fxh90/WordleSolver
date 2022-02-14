"""
Simulator for testing the solver of Wordle puzzles.
"""

import time
import numpy as np

import helper
import solver

__author__ = "Z Feng"

max_auto_attempts = 10


def simulator() -> float:
    """
    Simulator that goes through every possible Wordle puzzle in the dictionary, and compute the mean.
    :return: mean number of attempts by the solver.
    """
    attempts = []
    potential_answers = helper.get_answer_dictionary()
    for i, answer in enumerate(potential_answers[:10]):
        print(f'\n{i + 1}/{len(potential_answers)}')
        attempt = responder(answer, do_print=True)
        attempts.append(attempt)
    return float(np.mean(attempts))


def responder(answer: str, do_print: bool = False) -> int:
    """
    Respond to the solver to simulate the puzzle.
    :param answer: Right answer
    :param do_print: print progress or not
    :return: number of attempts used
    """
    if do_print:
        print(f'Simulation starts! Answer = {answer}')
        print('attempt\tguess\tpattern')
    gen = solver.auto_solver(strategy='score 1')
    guess = next(gen)
    for attempt in range(max_auto_attempts):
        if guess != answer:
            similarity = helper.compare(guess, answer)
            if do_print:
                pattern = helper.similarity_to_pattern(similarity)
                print(f'{attempt + 1}\t\t{guess}\t{pattern}')
        else:
            if do_print:
                print(f'{attempt + 1}\t\t{guess}\tCorrect!')
            return attempt + 1
        next(gen)
        guess = gen.send(similarity)


if __name__ == "__main__":
    t_start = time.time()
    mean = simulator()
    print(f'\nSolver finishes in {mean: .3f} attempts on average!')
    print(f'Finished in {time.time() - t_start: .3f} seconds!')

# EOF
