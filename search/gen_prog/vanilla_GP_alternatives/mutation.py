import math

from search.gen_prog.vanilla_GP_alternatives import general

import random
from common.prorgam import Program

# ------------------------------------------------ Start original code ------------------------------------------------

def classical_mutation(program, mutation_chance, token_functions):
    program_seq = program.sequence
    mutated_seq = []
    for function in program_seq:
        if (general.draw_from([True, False], weights=[mutation_chance, 100 - mutation_chance])):
            new_random_function = general.draw_from(token_functions)
            mutated_seq.append(new_random_function)
        else:
            mutated_seq.append(function)

    mutated_program = Program(mutated_seq)

    return mutated_program


def UMAD(program, token_functions):
    genome_initial = program.sequence
    genome_intermediate = []
    genome_final = []

    addRate = 0.09
    delRate = addRate / (addRate + 1)

    # Addition step
    for gene in genome_initial:
        if random.uniform(0, 1) < addRate:
            new_gene = general.draw_from(token_functions)
            if random.uniform(0, 1) < 0.5:
                genome_intermediate.append(new_gene)
                genome_intermediate.append(gene)
            else:
                genome_intermediate.append(gene)
                genome_intermediate.append(new_gene)
        else:
            genome_intermediate.append(gene)

    # Deletion step
    for gene in genome_intermediate:
        if random.uniform(0, 1) < delRate:
            continue
        else:
            genome_final.append(gene)

    new_program = Program(genome_final)
    return new_program

# ------------------------------------------------ End original code ------------------------------------------------


def one_mutation_mutation(program, token_functions):
    program_seq = program.sequence
    mutated_seq = []

    mutation_index = random.randint(0, len(program_seq) - 1)
    i = 0

    for function in program_seq:
        if i == mutation_index:
            mutated_seq.append(general.draw_from(token_functions))
        else:
            mutated_seq.append(function)
        i += 1

    mutated_program = Program(mutated_seq)

    return mutated_program


def one_mutation_mutation_altered(program, token_functions):
    program_seq = program.sequence
    mutated_seq = []

    mutation_index = random.randint(0, len(program_seq) + 1)
    i = 0

    for function in program_seq:
        if i == mutation_index:
            mutated_seq.append(general.draw_from(token_functions))
        else:
            mutated_seq.append(function)
        i += 1

    if mutation_index == (len(program_seq) + 1):
        mutated_seq.append(general.draw_from(token_functions))

    mutated_program = Program(mutated_seq)

    return mutated_program


# TODO: Fix this
def mutation_clock_mutation(gen, mutation_chance, token_functions):
    mutated_gen = []
    k = 1
    i = 1
    genlength = len(gen)

    while i < genlength:
        u = random.uniform(0, 1)
        l = (1 / mutation_chance) * math.log(1 - u, 10)
        program_seq = gen[i].sequence
        n = len(program_seq)
        mutation_index_k = ((k + l) % n)
        mutation_index_i = ((k + l) / n)

        # Mutate the gene

        k = round(mutation_index_k)
        i = i + round(mutation_index_i)

    return mutated_gen


def interchanging_mutation(program):
    program_seq = program.sequence
    mutated_seq = []

    mutation_index_first = random.randint(0, len(program_seq) - 1)
    mutation_index_second = random.randint(0, len(program_seq) - 1)

    if mutation_index_first > mutation_index_second:
        temp = mutation_index_first
        mutation_index_first = mutation_index_second
        mutation_index_second = temp

    i = 0
    function_at_first = None
    function_at_second = None

    for function in program_seq:
        if i == mutation_index_first:
            function_at_first = function
        if i == mutation_index_second:
            function_at_second = function
        i += 1

    i = 0
    for function in program_seq:
        if not i == mutation_index_first and not i == mutation_index_second:
            mutated_seq.append(function)
        if i == mutation_index_first:
            mutated_seq.append(function_at_second)
        if i == mutation_index_second and not i == mutation_index_first:
            mutated_seq.append(function_at_first)
        i += 1

    return Program(mutated_seq)


def scramble_mutation(program):
    program_seq = program.sequence
    mutated_seq = []

    mutation_index_first = random.randint(0, len(program_seq) - 1)
    mutation_index_second = random.randint(0, len(program_seq) - 1)

    if mutation_index_first > mutation_index_second:
        temp = mutation_index_first
        mutation_index_first = mutation_index_second
        mutation_index_second = temp

    temp = []

    i = 0
    for function in program_seq:
        if mutation_index_first <= i <= mutation_index_second:
            temp.append(function)
        if i > mutation_index_second:
            break
        i += 1

    random.shuffle(temp)

    i = 0
    pointer = 0
    for function in program_seq:
        if mutation_index_first <= i <= mutation_index_second:
            mutated_seq.append(temp[pointer])
            pointer += 1
        else:
            mutated_seq.append(function)
        i += 1
    return Program(mutated_seq)


def reversing_mutation(program):
    program_seq = program.sequence
    mutated_seq = []

    mutation_index_first = random.randint(0, len(program_seq) - 1)
    mutation_index_second = random.randint(0, len(program_seq) - 1)

    if mutation_index_first > mutation_index_second:
        temp = mutation_index_first
        mutation_index_first = mutation_index_second
        mutation_index_second = temp

    temp = []

    i = 0
    for function in program_seq:
        if mutation_index_first <= i <= mutation_index_second:
            temp.append(function)
        if i > mutation_index_second:
            break
        i += 1

    temp.reverse()

    i = 0
    pointer = 0
    for function in program_seq:
        if mutation_index_first <= i <= mutation_index_second:
            mutated_seq.append(temp[pointer])
            pointer += 1
        else:
            mutated_seq.append(function)
        i += 1

    return Program(mutated_seq)
