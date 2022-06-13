import random

from common.prorgam import Program
from common.tokens.abstract_tokens import EnvToken
from search.vlns.large_neighborhood_search.destroy.destroy import Destroy


class ExtractNDestroy(Destroy):
    """For each token in the program, an extraction will happen with probability p_extract. If an extraction occurs; a
    random N is selected from n_options according to weight distribution n_weight. N tokens, including the current
    token, will be removed from the sequence splitting the sequence.

    This destroy method runs in O(1).
    """

    def __init__(self, initial_max_n: int, max_max_n: int, strategy: str = "random"):
        """See class documentation."""
        assert initial_max_n >= 0

        super().__init__()

        self.initial_max_n = initial_max_n
        self.max_n = initial_max_n
        self.max_max_n = max_max_n
        self.strategy = strategy

    def reset(self):
        self.max_n = self.initial_max_n

    def destroy(self, program: Program, i: int = 0, Ni: int = 0) -> list[list[EnvToken]]:

        # Pick N
        mn = min(self.max_n, len(program.sequence))
        n = random.randint(0, mn + 1)
        if self.strategy == "increasing":
            # n is some increasing number between 0 and mn
            n = max(0, int((i/Ni)*mn))
        elif self.strategy == "decreasing":
            # n is some decreasing number between 0 and mn
            n = max(0, mn - int((i/Ni)*mn))

        # Pick index of first to be destroyed token
        i = random.randint(0, len(program.sequence) - n + 1)

        # Return slice of part before destroyed and after
        return [
            program.sequence[:i],
            program.sequence[i+n:]
        ]

    def increment_search_depth(self):
        if self.max_n != self.max_max_n:
            self.max_n += 1
