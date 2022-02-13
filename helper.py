"""
Helper functions for both simulator and solver.
"""

__author__ = "fxh90"

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

if __name__ == "__main__":
    print(compare('banana', 'target'))

#EOF