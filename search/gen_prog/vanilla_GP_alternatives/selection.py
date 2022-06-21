# Original code by F. Azimzade. Other code by M.R. Tromp.

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


def sum_fitness(current_gen):
    total_fitness = 0
    for (fit, _) in current_gen:
        total_fitness += fit

    return total_fitness


def stochastic_universal_sampling(current_gen):
    intermediate_gen = []
    N = len(current_gen)
    total_fitness = sum_fitness(current_gen)
    mean = (1/N) * total_fitness
    rand = random.uniform(0, mean)
    pointers = []

    for i in range(N):
        pointers.append(rand + (i * mean))

    for pointer in pointers:
        curr_sum = 0
        for f, program in current_gen:
            curr_sum += f
            if not curr_sum < pointer:
                intermediate_gen.append(program)
                break
    return intermediate_gen


def roulette_wheel_selection(gen):
    intermediate_gen = []
    total_fitness = sum_fitness(gen)
    N = len(gen)

    for i in range(N):
        pointer = random.uniform(0, total_fitness)
        curr_sum = 0
        for f, program in gen:
            curr_sum += f
            if not curr_sum < pointer:
                intermediate_gen.append(program)
                break
    return intermediate_gen


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
    for i in range(len(current_gen_errors)):
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


def downsampled_lexicase(current_gen, training_examples):
    examples = copy.deepcopy(training_examples)
    random.shuffle(examples)

    count = 0

    while (len(current_gen) > 1) and (len(examples) > 0) and (count < 5):
        example = examples.pop(0)
        (best_error, current_gen_errors) = find_best_error(current_gen, example)
        current_gen = find_with_error(current_gen, current_gen_errors, best_error)
        count += 1

    if len(current_gen) == 1:
        return current_gen[0]
    else:
        return random.choice(current_gen)


def downsampled_lexicase_selection(current_gen, training_examples):
    N = len(current_gen)

    intermediate_gen = []
    for i in range(N):
        intermediate_gen.append(downsampled_lexicase(current_gen, training_examples))

    return intermediate_gen


def combined_lexicase_selection(current_gen, training_examples, current_gen_fitness):
    training_size = len(training_examples)

    if training_size <= 4:
        return stochastic_universal_sampling(current_gen_fitness)
    else:
        return selection_lexicase(current_gen, training_examples)


def tournament_selection_selection(current_gen_fitness):
    k = 5
    N = len(current_gen_fitness)
    gen = copy.deepcopy(current_gen_fitness)

    intermediate_gen = []

    for i in range(N):
        random.shuffle(gen)
        tournament = []
        for j in range(k):
            tournament.append(gen[j])
        tournament.sort(reverse=True)
        fitness = tournament[0][0]
        equal_fitness = []

        for program in tournament:
            if(program[0] == fitness):
                equal_fitness.append(program[1])
            else:
                break

        intermediate_gen.append(random.choice(equal_fitness))

    return intermediate_gen


def truncation_selection_selection(current_gen):
    N = len(current_gen)
    p = 0.25
    select_quantity = int(N * p)
    select_iterations = int(1/p)

    intermediate_gen = []

    gen = copy.deepcopy(current_gen)
    gen.sort(reverse=True)

    for i in range(select_iterations):
        for j in range(select_quantity):
            intermediate_gen.append(gen[j][1])

    return intermediate_gen
