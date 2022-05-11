import copy

from search.gen_prog.vanilla_GP_alternatives import general
from search.gen_prog.vanilla_GP_alternatives import fitness

import math
import statistics
import random, itertools
from common.experiment import Example
from common.prorgam import Program
from common.tokens.abstract_tokens import InvalidTransition, Token
from common.tokens.control_tokens import LoopIterationLimitReached
from search.abstract_search import SearchAlgorithm
from search.invent import invent2

from typing import List
from math import inf

# ------------------------------------------------ Start original code ------------------------------------------------

# I don't think this is used so I do not want to spend the time necessary to fix this.
def selection(current_gen_fitness):
    intermediate_gen = []
    crossover_subset = []

    probs = general.normalize_fitness(current_gen_fitness)
    for i in range(len(current_gen_fitness)):
        _, program = current_gen_fitness[i]
        prob = probs[i]
        chosen = general.chose_with_prob(prob)
        if (chosen):
            intermediate_gen.append(program)
            continue
        crossover_subset.append(program)

    # MAKE SURE THAT CROSSOVER SUBSET HAS EVEN NUMBER OF ELEMENTS
    if (len(crossover_subset) % 2 != 0):
        intermediate_gen.append(crossover_subset[0])
        crossover_subset = crossover_subset[1:]

    children = []
    random.shuffle(crossover_subset)
    for program_x, program_y in general.pairs_from(crossover_subset):
        child_x, child_y = general.one_point_crossover(program_x, program_y)
        children.append(child_x)
        children.append(child_y)

    intermediate_gen = intermediate_gen + children

    return intermediate_gen


def SUS(N, gen_probabilities):
    stepsize = 1.0 / N
    pointer = random.uniform(0, 1)

    wheel = general.roulette_wheel(gen_probabilities)

    selected_programs = general.select_N_on_wheel(wheel, N, stepsize, pointer)

    return selected_programs


def selection_SUS(current_gen_fitness):
    N = len(current_gen_fitness)
    gen_probabilities = general.normalize_fitness(current_gen_fitness)

    intermediate_gen = []
    intermediate_gen = SUS(N, gen_probabilities)
    random.shuffle(intermediate_gen)  # for extra stochasticity

    return intermediate_gen

# ------------------------------------------------ End original code ------------------------------------------------


def find_best_error(current_gen, example):
    best = float("inf")
    current_gen_errors = []
    for program in current_gen:
        error = fitness.program_error_example(program, example)
        current_gen_errors.append(error)
        if error < best:
            best = error
    return (best, current_gen_errors)


def find_with_error(current_gen, current_gen_errors, error):
    programs_with_error = []
    for i in range(len(current_gen_errors) - 1):
        if current_gen_errors[i] == error:
            programs_with_error.append(current_gen[i])
    return programs_with_error


def lexicase(current_gen, training_examples):
    examples = copy.deepcopy(training_examples)
    random.shuffle(examples)

    while (len(current_gen) > 1) and (len(examples) > 0):
        example = examples.pop(0)
        (best_error, current_gen_errors) = find_best_error(current_gen, example)
        current_gen = find_with_error(current_gen, current_gen_errors, best_error)

    if len(current_gen) == 1:
        return current_gen[0]
    else:
        return random.choice(current_gen)


def selection_lexicase(current_gen, training_examples):
    N = len(current_gen)

    intermediate_gen = []
    for i in range(N):
        intermediate_gen.append(lexicase(current_gen, training_examples))

    return intermediate_gen
