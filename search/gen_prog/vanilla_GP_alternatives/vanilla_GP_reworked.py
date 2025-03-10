# VANILLA GENETIC PROGRAMMING ALGORITHM Original code by F. Azimzade, but refactored by M.R. Tromp.
import enum

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
from common.tokens.abstract_tokens import Token
from search.abstract_search import SearchAlgorithm
from search.invent import invent2

from typing import List


class SelectionMethods(enum.Enum):
    SUSOriginal = 1
    SUS = 2
    RWS = 3
    Lexicase = 4
    DownsampledLexicase = 5
    CombinedLexicase = 6
    Tournament = 7
    Truncation = 8


class CrossoverMethods(enum.Enum):
    OnePoint = 1
    NPoint = 2
    TwoPoint = 3
    Uniform = 4
    QueenBee = 5
    ThreeParent = 6
    MultipleParent = 7
    Random = 8


class MutationMethods(enum.Enum):
    Classical = 1
    UMAD = 2
    OneMutation = 3
    AlteredOneMutation = 4
    Interchanging = 5
    Scramble = 6
    Reversing = 7
    AlteredOneMutationLoops = 8


class VanillaGPReworked(SearchAlgorithm):
    # Static fields
    selection_type = SelectionMethods.DownsampledLexicase
    crossover_type = CrossoverMethods.ThreeParent
    mutation_type = MutationMethods.AlteredOneMutationLoops

    MAX_NUMBER_OF_GENERATIONS = 200
    MAX_TOKEN_FUNCTION_DEPTH = 5  # used in the invention of tokens
    training_examples = []  # training examples
    token_functions = []
    loop_token_functions = []
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
        new_gen = []

        if self.selection_type == SelectionMethods.SUSOriginal:
            new_gen = selection.selection_SUS(gen)

        elif self.selection_type == SelectionMethods.SUS:
            new_gen = selection.stochastic_universal_sampling(gen)

        elif self.selection_type == SelectionMethods.RWS:
            new_gen = selection.roulette_wheel_selection(gen)

        elif self.selection_type == SelectionMethods.Lexicase:
            new_gen = selection.selection_lexicase(self.current_gen, self.training_examples)

        elif self.selection_type == SelectionMethods.DownsampledLexicase:
            new_gen = selection.downsampled_lexicase_selection(self.current_gen, self.training_examples)

        elif self.selection_type == SelectionMethods.CombinedLexicase:
            new_gen = selection.combined_lexicase_selection(self.current_gen, self.training_examples, gen)

        elif self.selection_type == SelectionMethods.Tournament:
            new_gen = selection.tournament_selection_selection(gen)

        elif self.selection_type == SelectionMethods.Truncation:
            new_gen = selection.truncation_selection_selection(gen)

        return new_gen

    def gen_crossover(self, gen):
        children = []

        if self.crossover_type == CrossoverMethods.QueenBee:
            children = crossover.queen_bee_crossover(gen)

        elif self.crossover_type == CrossoverMethods.ThreeParent:
            children = crossover.three_parent_crossover(gen)

        elif self.crossover_type == CrossoverMethods.MultipleParent:
            children = crossover.multiple_parent_crossover(gen)

        elif self.crossover_type == CrossoverMethods.Random:
            children = crossover.random_crossover(gen)

        else:
            i = 0
            while i < len(gen):
                program_x, program_y = gen[i], gen[i + 1]
                child_x, child_y = None, None

                if self.crossover_type == CrossoverMethods.OnePoint:
                    child_x, child_y = crossover.one_point_crossover(program_x, program_y)

                elif self.crossover_type == CrossoverMethods.NPoint:
                    child_x, child_y = crossover.n_point_crossover(program_x, program_y)

                elif self.crossover_type == CrossoverMethods.TwoPoint:
                    child_x, child_y = crossover.two_point_crossover(program_x, program_y)

                elif self.crossover_type == CrossoverMethods.Uniform:
                    child_x, child_y = crossover.uniform_crossover(program_x, program_y)

                children.append(child_x)
                children.append(child_y)
                i += 2
        return children

    def gen_mutate(self, gen):
        mutated_gen = []

        if self.mutation_type == MutationMethods.Classical:
            mutated_gen = [mutation.classical_mutation(program, self.mutation_chance, self.token_functions) for program
                           in gen]

        elif self.mutation_type == MutationMethods.UMAD:
            mutated_gen = [mutation.UMAD(program, self.token_functions) for program in gen]

        elif self.mutation_type == MutationMethods.OneMutation:
            mutated_gen = [mutation.one_mutation_mutation(program, self.token_functions) for program in gen]

        elif self.mutation_type == MutationMethods.AlteredOneMutation:
            mutated_gen = [mutation.one_mutation_mutation_altered(program, self.token_functions) for program in gen]

        elif self.mutation_type == MutationMethods.Interchanging:
            mutated_gen = [mutation.interchanging_mutation(program) for program in gen]

        elif self.mutation_type == MutationMethods.Scramble:
            mutated_gen = [mutation.scramble_mutation(program) for program in gen]

        elif self.mutation_type == MutationMethods.Reversing:
            mutated_gen = [mutation.reversing_mutation(program) for program in gen]

        elif self.mutation_type == MutationMethods.AlteredOneMutationLoops:
            mutated_gen = [mutation.one_mutation_mutation_altered_higher_loop_chance(program, self.token_functions, self.loop_token_functions) for program in gen]

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

        for token in self.token_functions:
            if "while" in token.to_formatted_string():
                self.loop_token_functions.append(token)

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
