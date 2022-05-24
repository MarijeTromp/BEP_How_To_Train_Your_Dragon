# VANILLA GENETIC PROGRAMMING ALGORITHM

from search.gen_prog.vanilla_GP_alternatives import general
from search.gen_prog.vanilla_GP_alternatives import fitness
from search.gen_prog.vanilla_GP_alternatives import selection
from search.gen_prog.vanilla_GP_alternatives import crossover
from search.gen_prog.vanilla_GP_alternatives import mutation

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


class VanillaGPReworked(SearchAlgorithm):
    # Static fields
    type = "UN"
    MAX_NUMBER_OF_GENERATIONS = 200
    MAX_TOKEN_FUNCTION_DEPTH = 5  # used in the invention of tokens
    training_examples = []  # training examples
    token_functions = []
    mutation_chance = 2  # Chance of an individual gene(function) being mutated (may be changed to be random for each mutation(?))

    # Dynamic fields
    current_gen_num = 0
    current_gen_fitness = []

    _best_fitness = float("inf")
    _best_solved = 1

    # Genetic Algorithm

    def generate_rand_program(self, max_prog_length):
        prog_length = random.randint(1, max_prog_length)
        program_seq = []
        program_seq = general.draw_from(self.token_functions, number_of_elems=prog_length)
        return Program(program_seq)

    def generate_rand_population(self, population_size, max_prog_length):
        population = []
        for i in range(population_size):
            program = self.generate_rand_program(max_prog_length)
            population.append(program)
        return population

    def gen_selection(self, gen):
        new_gen = selection.selection_SUS(gen)
        return new_gen

    def gen_crossover(self, gen):
        children = []

        return crossover.multiple_parent_crossover(gen)

        # TODO: If queen bee or three parent, do that instead of do something for every pair of programs
        # Iterate over the programs by 2 to pair them up
        i = 0
        while i < len(gen):
            program_x, program_y = gen[i], gen[i + 1]
            child_x, child_y = None, None
            if (self.type == "O" or self.type == "U"):
                child_x, child_y = crossover.one_point_crossover(program_x, program_y)
            else:
                child_x, child_y = crossover.n_point_crossover(program_x, program_y)
            children.append(child_x)
            children.append(child_y)
            i += 2
        return children

    def gen_mutate(self, gen):
        mutated_gen = []
        if (self.type == "O" or self.type == "N"):
            mutated_gen = [mutation.classical_mutation(program, self.mutation_chance, self.token_functions) for program in gen]
        else:
            mutated_gen = [mutation.UMAD(program, self.token_functions) for program in gen]
        return mutated_gen

    # -- Breed Next Generation
    def breed_generation(self, current_gen_fitness):
        new_gen = self.gen_selection(current_gen_fitness)
        new_gen = self.gen_crossover(new_gen)
        new_gen = self.gen_mutate(new_gen)
        self.current_gen_num += 1
        return new_gen

    # General Interface

    def __init__(self, time_limit_sec: float):
        super().__init__(time_limit_sec)

    def extend_result(self, search_result):
        search_result.dictionary['initial_error'] = self.initial_error
        return super().extend_result(search_result)

    def setup(self, training_examples: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]):
        self.token_functions = [token for token in list(trans_tokens)] + invent2(trans_tokens, bool_tokens,
                                                                                 self.MAX_TOKEN_FUNCTION_DEPTH)
        self.training_examples = training_examples

        # Set the overall best results to the performance of the initial (empty) best program Program([])
        self._best_error, self._best_program = fitness.evaluate_program(self._best_program, self.training_examples)

        # Record the initial error (error of the empty program) in the SearchResult
        self.initial_error = self._best_error

        # Parameters for the initial random population
        self.initial_population_size = 200
        self.max_prog_length = 10

        # print("Type =", self.type)
        # print("Max Number of Generations", self.MAX_NUMBER_OF_GENERATIONS)
        # print("Population size =", self.initial_population_size)
        # print("Max Program Length =", self.max_prog_length)

        # The current generation is the initial random generation at the beginning
        initial_gen = self.generate_rand_population(self.initial_population_size, self.max_prog_length)
        self.current_gen = initial_gen

        self.current_gen_num = 0
        self.number_of_iterations = 0
        self.number_of_explored_programs = self.initial_population_size
        self.cost_per_iteration = []

    def iteration(self, training_example: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]) -> bool:
        # Collect statistics about generation

        # Calculate the error for each program in the current generation
        current_gen_error = fitness.gen_error(self.current_gen, self.training_examples)

        self.number_of_explored_programs += len(self.current_gen)

        # Get the program with the lowest error
        current_best_error, current_best_program = current_gen_error[0]
        self.cost_per_iteration.append((self.current_gen_num, current_best_error))

        if (str(current_best_error) == "0" or current_best_error < self._best_error):
            self._best_error = current_best_error
            self._best_program = current_best_program

        if (str(current_best_error) == "0" or self.current_gen_num >= self.MAX_NUMBER_OF_GENERATIONS):
            return False

        current_gen_fitness = fitness.gen_fitness(current_gen_error)

        # print("----Gen ", self.current_gen_num, "----")
        # generation_stats(current_gen_fitness)

        next_gen = self.breed_generation(current_gen_fitness)
        self.current_gen = next_gen

        self.number_of_iterations += 1

        return True
