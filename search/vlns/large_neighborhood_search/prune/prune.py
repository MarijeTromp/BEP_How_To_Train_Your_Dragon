from common.prorgam import Program

"""
determines the observational equivalence
p1: first program to be compared
p2: second program to be compared
dom: domain to compare them in
frac: fraction of example to take for comparison
"""
def prune(p1: Program, p2: Program, dom: str, frac: float) -> bool:
    #TODO: implement observational equivalence testing
    #TODO: add the chance of being pruned in here, so it saves an if-condition in LNS
    #QUESTION: how do we get an output state of a program? --> abstract_search.cost() method
    #--> p.interp(input_environment) --> returns an Environment object
    #this is already called in effective cost, so we could avoid calling this again?
    #also: an easier/more lightweight variant would be to compare the cost of the entire test case
    #   instead of each environment in the test case (which would take forever?)
    #so if each cost for each example in a test case is equal, it is likely observationally equivalent
    #(but not necerssarily because different environments COULD have the same costs)
    return False