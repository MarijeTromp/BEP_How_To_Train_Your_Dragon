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
