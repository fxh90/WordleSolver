"""
Helper functions for both simulator and solver.
"""

__author__ = "Z Feng"

def compare(guess: str, target: str) -> int:
    """
    Compare a guess string to a target string. Return the similarity as an integer in the range of [0, 3^N-1], where
    N is the length of both guess and target strings.
    """
    assert len(guess) == len(target)
    N = len(guess)
    similarity = 0
    for i in range(N):
        if guess[i] == target[i]:
            similarity += 2 * 3 ** i
        elif guess[i] in target:
            similarity += 3 ** i
    assert 0 <= similarity < 3 ** N
    return similarity


def get_guess_dictionary() -> list:
    with open('words_wordle.txt', 'r') as f:
        dictionary = f.readlines()
    for i in range(len(dictionary)):
        # print(len(word))
        assert len(dictionary[i]) == 6
        dictionary[i] = dictionary[i][:5]
    return dictionary


def get_answer_dictionary() -> list:
    with open('words_wordle_solutions.txt', 'r') as f:
        dictionary = f.readlines()
    for i in range(len(dictionary)):
        # print(len(word))
        assert len(dictionary[i]) == 6
        dictionary[i] = dictionary[i][:5]
    return dictionary


if __name__ == "__main__":
    guess_dict = get_answer_dictionary()
    print(len(guess_dict))

#EOF