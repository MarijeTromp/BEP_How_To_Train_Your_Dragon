from typing import Callable, List, Tuple
from common.tokens.abstract_tokens import InvalidTransition, Token
from common.prorgam import Program
from common.experiment import Example, TestCase
from search.abstract_search import SearchAlgorithm
from common.tokens.control_tokens import If, LoopIterationLimitReached, LoopWhile
import random
import math

from search.search_result import SearchResult

random.seed(5099404)

class Mutation():
    def __init__(self, name: str, fun: Callable[[Program], Program]):
        self.name = name
        self.fun: Callable[[Program], Program] = fun

    # Doesn't change the input argument, since the callback never modifies the original Program!
    def apply(self, program: Program) -> Program:
        return self.fun(program)


class MetropolisHasting(SearchAlgorithm):
    def __init__(self, time_limit_sec: float, params: dict = {}):

        # Default parameters
        mutation_params: dict = {
            "type": "metropolis",
            "alpha": 1,
            "add_token_end": 0,
            "add_token_random": 0,
            "remove_token_end": 0,
            "remove_token_random": 0,
            "add_loop_end": 0,
            "add_loop_random": 0,
            "add_if_statement_end": 0,
            "add_if_statement_random": 0,
            "start_over": 0
        }

        for k,v in params.items():
            mutation_params[k] = v

        super().__init__(time_limit_sec, mutation_params)

    def setup(self, examples: List[Example], trans_tokens, bool_tokens):
        self.number_of_explored_programs = 0
        self.number_of_iterations = 0
        self.cost_per_iteration = []
        self._best_program: Program = Program([])
        self.cost = 100
        self.proposal_distribution = ProposalDistribution()
        # Find a way to systematically explore the types of mutations and their values,
        # e.g. remove_random_token vs remove_last_token
        fac = MutationFactory()
        self.proposal_distribution.add_mutation(fac.add_token_end(trans_tokens), self.params['add_token_end'])
        self.proposal_distribution.add_mutation(fac.add_token_random(trans_tokens), self.params['add_token_random'])

        self.proposal_distribution.add_mutation(fac.remove_token_end(), self.params['remove_token_end'])
        self.proposal_distribution.add_mutation(fac.remove_token_random(), self.params['remove_token_random'])

        self.proposal_distribution.add_mutation(fac.add_loop_end(bool_tokens, trans_tokens), self.params['add_loop_end'])
        self.proposal_distribution.add_mutation(fac.add_loop_random(bool_tokens, trans_tokens), self.params['add_loop_random'])

        self.proposal_distribution.add_mutation(fac.add_if_statement_end(bool_tokens, trans_tokens), self.params['add_if_statement_end'])
        self.proposal_distribution.add_mutation(fac.add_if_statement_random(bool_tokens, trans_tokens), self.params['add_if_statement_random'])

        self.proposal_distribution.add_mutation(fac.start_over(), self.params['start_over'])

    def iteration(self, examples: List[Example], trans_tokens, bool_tokens) -> bool:
        self.number_of_iterations += 1
        self.number_of_explored_programs += 1
        mut: Mutation = self.proposal_distribution.sample()
        forward_transition, backward_transition = self.calc_transition_probabilities(mut)

        self._best_program, newcost, solved = MetropolisHasting.maybe_apply_mutation(
            examples, self._best_program, self.cost, mut, forward_transition, backward_transition, self.params['alpha'], self.params['type'])

        if (newcost != self.cost):
            self.cost_per_iteration.append((self.number_of_iterations, newcost))

        self.cost = newcost
        return not solved

    def extend_result(self, search_result: SearchResult):
        return super().extend_result(search_result)

    def calc_transition_probabilities(self, mut: Mutation):
        total = self.proposal_distribution.get_total_weight()
        forward_transition, backward_transition = 0, 0

        # Examine math to find proper forward and backward probabilities for random position mutations
        # Current approach: just use metropolis (assume forward == backward)
        if mut.name == "add_token_end":
            pro = self.params['add_token_end'], self.params['remove_token_end']
        elif mut.name == "add_token_random":
            pro = self.params['add_token_random'], self.params['remove_token_random']
        elif mut.name == "remove_token_end":
            pro = self.params['remove_token_end']
        elif mut.name == "remove_token_random":
            return 1, 1
        elif mut.name == "add_loop_end":
            pro = self.params['add_loop_end']
        elif mut.name == "add_if_statement_end":
            pro = self.params['add_if_statement_end']
        elif mut.name == "start_over":
            # Explore alternatives for restarts
            return 1, 1

        return forward_transition / total, backward_transition / total


    @staticmethod
    def maybe_apply_mutation(examples: List[Example], old_program: Program, ocost: int, mut: Mutation,
                             forward_transition, backward_transition, alpha: float, type: str) -> Tuple[Program, int, int]:
        new_program = mut.apply(old_program)
        try:
            cost = 0

            for case in examples:
                nenv = new_program.interp(case.input_environment)
                cost += abs(nenv.distance(case.output_environment))
            solved = False

            # 0.1 for rounding errors, all distance measures should return integer values
            if cost < 0.1:
                solved = True
                for case in examples:
                    nenv = new_program.interp(case.input_environment)
                    solved = solved and nenv.correct(case.output_environment)

            # Default is Random Walk - Metropolis
            ratio = math.exp(-alpha * cost) / math.exp(-alpha * ocost)
            if type == "metropolis_hastings":
                ratio *= forward_transition / backward_transition

            if ratio > 1:
                return new_program, cost, solved
            if random.random() < ratio:
                return new_program, cost, solved
            return old_program, ocost, False

        except(InvalidTransition, LoopIterationLimitReached):
            return old_program, ocost, False




class ProposalDistribution():
    def __init__(self):
        self.mutations: List[Mutation] = []

    def add_mutation(self, mut: Mutation, pro: int):
        self.mutations.append((mut, pro))

    def sample(self) -> Mutation:
        # get total probability
        tot = 0
        for _, pro in self.mutations:
            tot += pro
        choice = random.randrange(tot)

        for mut, pro in self.mutations:
            if choice < pro:
                return mut
            choice -= pro

    def get_total_weight(self):
        return sum([mut[1] for mut in self.mutations])

# The operation must never be allowed to modify the Program that is passed in!
class MutationFactory():
    def __init__(self):
        pass

    # Adds a random token to the end of the program
    def add_token_end(self, trans_tokens) -> Mutation:
        def operation(pro: Program) -> Program:
            rand_token = random.choice(list(trans_tokens))
            return Program(pro.sequence + [rand_token])

        return Mutation("add_token_end", operation)

    # Adds a random token in a random position in the program
    def add_token_random(self, trans_tokens) -> Mutation:
        def operation(pro: Program) -> Program:
            rand_token = random.choice(list(trans_tokens))

            length = len(pro.sequence)
            if length == 0:
                return Program([rand_token])
            idk = random.randrange(length + 1)

            return Program(pro.sequence[:idk] + [rand_token] + pro.sequence[idk:])

        return Mutation("add_token_random", operation)

    # Removes the last token in the program
    def remove_token_end(self) -> Mutation:
        def operation(pro: Program) -> Program:
            return Program(pro.sequence[:len(pro.sequence) - 1])

        return Mutation("remove_token_end", operation)

    # Removes a random token from the program
    def remove_token_random(self) -> Mutation:
        def operation(pro: Program) -> Program:
            length = len(pro.sequence)
            if length == 0:
                return pro
            idk = random.randrange(length)
            return Program(pro.sequence[:idk] + pro.sequence[idk + 1:])

        return Mutation("remove_token_random", operation)


    def add_loop_end(self, bool_tokens, trans_tokens) -> Mutation:
        def operation(pro: Program) -> Program:
            rand_bool = random.choice(list(bool_tokens))
            rand_token = random.choice(list(trans_tokens))
            return Program(pro.sequence + [LoopWhile(rand_bool, [rand_token])])

        return Mutation("add_loop_end", operation)

    def add_loop_random(self, bool_tokens, trans_tokens) -> Mutation:
        def operation(pro: Program) -> Program:
            rand_bool = random.choice(list(bool_tokens))
            rand_token = random.choice(list(trans_tokens))

            length = len(pro.sequence)
            if length == 0:
                return Program([LoopWhile(rand_bool, [rand_token])])
            idk = random.randrange(length + 1)

            return Program(pro.sequence[:idk] + [LoopWhile(rand_bool, [rand_token])] + pro.sequence[idk:])

        return Mutation("add_loop_random", operation)


    def add_if_statement_end(self, bool_tokens, trans_tokens) -> Mutation:
        def operation(pro: Program) -> Program:
            rand_bool = random.choice(list(bool_tokens))
            rand_token = random.choice(list(trans_tokens))
            rand_token2 = random.choice(list(trans_tokens))
            return Program(pro.sequence + [If(rand_bool, [rand_token], [rand_token2])])

        return Mutation("add_if_statement_end", operation)


    def add_if_statement_random(self, bool_tokens, trans_tokens) -> Mutation:
        def operation(pro: Program) -> Program:
            rand_bool = random.choice(list(bool_tokens))
            rand_token = random.choice(list(trans_tokens))
            rand_token2 = random.choice(list(trans_tokens))

            length = len(pro.sequence)
            if length == 0:
                return Program([If(rand_bool, [rand_token], [rand_token2])])
            idk = random.randrange(length + 1)

            return Program(pro.sequence[:idk] + [If(rand_bool, [rand_token], [rand_token2])] + pro.sequence[idk:])

        return Mutation("add_if_statement_random", operation)


    def start_over(self) -> Mutation:
        def operation(_: Program) -> Program:
            return Program([])

        return Mutation("start_over", operation)
