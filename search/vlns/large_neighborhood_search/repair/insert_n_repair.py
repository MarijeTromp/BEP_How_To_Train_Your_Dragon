import random

from common.prorgam import Program
from common.tokens.abstract_tokens import EnvToken
from search.vlns.large_neighborhood_search.repair.repair import Repair


class InsertNRepair(Repair):

    def __init__(self, initial_max_n, max_max_n: int, w_trans: float, w_if: float, w_loop: float, strategy: str = "random"):
        assert initial_max_n >= 0

        super().__init__()

        self.initial_max_n = initial_max_n
        self.max_n = initial_max_n
        self.max_max_n = max_max_n

        self.w_trans = w_trans
        self.w_if = w_if
        self.w_loop = w_loop
        self.strategy = strategy

    def repair(self, seqs: list[list[EnvToken]], i: int = 0, Ni: int = 0) -> Program:
        assert len(seqs) == 2

        seq = seqs[0]

        # Pick N, minimum of 1
        n = random.randint(1, self.max_n + 1)
        if self.strategy == "increasing":
            # n is some increasing number between 0 and self.max_n
            n = max(0, int((i/Ni)*self.max_n))
        elif self.strategy == "decreasing":
            # n is some decreasing number between 0 and self.max_n
            n = max(0, self.max_n - int((i/Ni)*self.max_n))

        for _ in range(n):
            seq.append(self.random_token(w_trans=self.w_trans, w_if=self.w_if, w_loop=self.w_loop))

        seq.extend(seqs[1])

        return Program(seq)

    def reset(self):
        self.max_n = self.initial_max_n

    def increment_search_depth(self):
        if self.max_n != self.max_max_n:
            self.max_n += 1
