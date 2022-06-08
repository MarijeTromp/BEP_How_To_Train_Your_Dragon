import random

from common.experiment import Example
from common.prorgam import Program
from common.tokens.abstract_tokens import InvalidTransition
from common.tokens.control_tokens import LoopIterationLimitReached
from search.vlns.large_neighborhood_search.prune.equivalence_classes import Equivalence_Classes

"""
determines the observational equivalence
p1: first program to be compared
p2: second program to be compared
dom: domain to compare them in
frac: fraction of example to take for comparison
"""

"""
def pruneList(p1: Program, p2: Program, test_case: list[Example], frac: float) -> bool:
    #TODO: test_case is always a list of one element, why? I don't know, seems weird

    sample_list = random.sample(test_case, int(frac*len(test_case)))
    print(len(test_case))
    print(sample_list)
    costs_p1 = cost(sample_list, p1)
    costs_p2 = cost(sample_list, p2)

    overlap = [i for i, j in zip(costs_p1, costs_p2) if i == j]
    frac_overlap = len(overlap)/len(sample_list)

    chance = frac_overlap #TODO: this has to be a better motivated chance, not just equal to the overlap
    if random.uniform(0, 1) > chance: # should this be < or >?
        return True

    return False
"""

def mediumprune(p1: Program, test_case: list[Example], eq_classes: Equivalence_Classes) -> bool:

    if len(test_case) != 1:
        return False #we have some different case than expected, so we do not prune to be safe
    cost_p1: int = int(cost(test_case, p1)[0])

    count = eq_classes.get_count(test_case[0].input_environment, cost_p1)

    if random.uniform(0, 1) >= 1/count: #TODO: improve this chance to something more motivated
        return True
    return False


def simpleprune(p1: Program, p2: Program, test_case: list[Example]) -> bool:

    cost_p1 = cost(test_case, p1)
    cost_p2 = cost(test_case, p2)

    chance = 0.5  # TODO: this has to be a better motivated chance, not just 0.5
    if (cost_p1 == cost_p2) & (random.uniform(0, 1) > chance):  # should this be < or >?
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