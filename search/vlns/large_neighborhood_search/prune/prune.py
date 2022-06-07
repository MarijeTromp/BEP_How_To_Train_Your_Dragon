import random

from common.experiment import Example
from common.prorgam import Program
from common.tokens.abstract_tokens import InvalidTransition
from common.tokens.control_tokens import LoopIterationLimitReached

"""
determines the observational equivalence
p1: first program to be compared
p2: second program to be compared
dom: domain to compare them in
frac: fraction of example to take for comparison
"""
def prune(p1: Program, p2: Program, test_case: list[Example], frac: float) -> bool:

    sample_list = random.sample(test_case, int(frac*len(test_case)))
    costs_p1 = cost(sample_list, p1)
    costs_p2 = cost(sample_list, p2)

    overlap = [i for i, j in zip(costs_p1, costs_p2) if i == j]
    frac_overlap = len(overlap)/len(sample_list)

    chance = frac_overlap #TODO: this has to be a better motivated chance, not just equal to the overlap
    if random.uniform(0, 1) > chance: # should this be < or >?
        return True

    return False

    #QUESTION: how do we get an output state of a program? --> abstract_search.cost() method
    #--> p.interp(input_environment) --> returns an Environment object
    #this is already called in effective cost, so we could avoid calling this again?
    #also: an easier/more lightweight variant would be to compare the cost of the entire test case
    #   instead of each environment in the test case (which would take forever?)
    #so if each cost for each example in a test case is equal, it is likely observationally equivalent
    #(but not necessarily because different environments COULD have the same costs)



# replica of the staticmethod cost in abstract_search
def cost(exs: list[Example], p: Program):
    def ex_cost(ex: Example):
        try:
            return p.interp(ex.input_environment).distance(ex.output_environment)
        except (InvalidTransition, LoopIterationLimitReached):
            return float('inf')

    return [ex_cost(ex) for ex in exs]