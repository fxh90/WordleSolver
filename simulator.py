"""
Simulator for testing the solver of Wordle puzzles.
"""

import helper
import solver

__author__ = "Z Feng"

max_auto_attempts = 10

def responder(answer: str, do_print: bool = False) -> int:
    """
    Respond to the solver to simulate the puzzle.
    :param answer: Right answer
    :param do_print: print progress or not
    :return: number of attempts used
    """
    if do_print:
        print(f'\nSimulation starts! Answer = {answer}')
        print('attempt\tguess\tpattern')
    gen = solver.auto_solver()
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
    attempts = responder('robin', do_print=True)
    print(f'finished in {attempts} attempts!')

# EOF
