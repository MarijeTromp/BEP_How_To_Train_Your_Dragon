import copy

from search.gen_prog.vanilla_GP_alternatives import general

import random, itertools
from common.prorgam import Program

# ------------------------------------------------ Start original code ------------------------------------------------


def pick_crossover_point(program):
    indices = range(0, len(program.sequence))
    chosen_index = general.draw_from(indices)
    return chosen_index


def one_point_crossover(program_x, program_y):
    seq_x = program_x.sequence
    seq_y = program_y.sequence

    if (len(seq_x) == 0 or len(seq_y) == 0):
        return program_x, program_y

    crossover_point_x = pick_crossover_point(program_x)
    crossover_point_y = pick_crossover_point(program_y)

    # print(crossover_point_x)
    # print(crossover_point_y)

    updated_seq_x = seq_x[:crossover_point_x + 1] + seq_y[crossover_point_y + 1:]
    updated_seq_y = seq_y[:crossover_point_y + 1] + seq_x[crossover_point_x + 1:]

    child_x = Program(updated_seq_x)
    child_y = Program(updated_seq_y)

    return child_x, child_y


def n_point_crossover(program_x, program_y):
    # Assumptions:
    # - points are sorted increasingly
    # - points are within range
    # - size of both point arrays is n
    # - points are unique

    seq_x = program_x.sequence
    seq_y = program_y.sequence

    # print(len(seq_x))
    # print(len(seq_y))

    min_length = min(len(seq_x), len(seq_y))
    if (min_length <= 1):
        return program_x, program_y

    n = random.randint(1, int(min_length / 2))
    # print("n =", n)

    x_points = sorted(random.sample(range(0, len(seq_x)), n))
    y_points = sorted(random.sample(range(0, len(seq_y)), n))

    # print("x_points =", x_points)
    # print("y_points =", y_points)

    cuts_x = []
    cuts_y = []

    start = 0
    for i in x_points:
        slice_i = seq_x[start:i + 1]
        cuts_x.append(slice_i)
        start = i + 1
    slice_tail = seq_x[start:]
    cuts_x.append(slice_tail)

    start = 0
    for i in y_points:
        slice_i = seq_y[start:i + 1]
        cuts_y.append(slice_i)
        start = i + 1
    slice_tail = seq_y[start:]
    cuts_y.append(slice_tail)

    # print("cuts_x = ", cuts_x)
    # print("cuts_y = ", cuts_y)

    for i in range(0, n + 1):
        if (i % 2 != 0):
            inter = cuts_x[i]
            cuts_x[i] = cuts_y[i]
            cuts_y[i] = inter

    child_x_seq = list(itertools.chain.from_iterable(cuts_x))
    child_y_seq = list(itertools.chain.from_iterable(cuts_y))

    # print(len(child_x_seq))
    # print(len(child_y_seq))

    child_x = Program(child_x_seq)
    child_y = Program(child_y_seq)

    return child_x, child_y

# ------------------------------------------------ End original code ------------------------------------------------


def two_point_crossover(program_x, program_y):
    seq_x = program_x.sequence
    seq_y = program_y.sequence

    if len(seq_x) == 0 or len(seq_x) == 1 or len(seq_y) == 0 or len(seq_y) == 1:
        return program_x, program_y

    crossover_point_x1 = pick_crossover_point(program_x)
    crossover_point_x2 = pick_crossover_point(program_x)
    crossover_point_y1 = pick_crossover_point(program_y)
    crossover_point_y2 = pick_crossover_point(program_y)

    while crossover_point_x1 == crossover_point_x2:
        crossover_point_x2 = pick_crossover_point(program_x)

    while crossover_point_y1 == crossover_point_y2:
        crossover_point_y2 = pick_crossover_point(program_y)

    if crossover_point_x1 > crossover_point_x2:
        temp = crossover_point_x1
        crossover_point_x1 = crossover_point_x2
        crossover_point_x2 = temp

    if crossover_point_y1 > crossover_point_y2:
        temp = crossover_point_y1
        crossover_point_y1 = crossover_point_y2
        crossover_point_y2 = temp

    updated_seq_x = seq_x[:crossover_point_x1 + 1] + seq_y[crossover_point_y1 + 1:crossover_point_y2 + 1] + seq_x[crossover_point_x2 + 1:]
    updated_seq_y = seq_y[:crossover_point_y1 + 1] + seq_x[crossover_point_x1 + 1:crossover_point_x2 + 1] + seq_x[crossover_point_y2 + 1:]

    child_x = Program(updated_seq_x)
    child_y = Program(updated_seq_y)

    return child_x, child_y

# TODO: Seems to be VERY slow
def uniform_crossover(program_x, program_y):
    shortest = program_x.sequence
    longest = program_y.sequence

    if len(longest) < len(shortest):
        temp = longest
        longest = shortest
        shortest = temp

    min_length = len(shortest)
    max_length = len(longest)

    if (min_length <= 1):
        return program_x, program_y

    length_child_x = random.randint(min_length, max_length)
    length_child_y = random.randint(min_length, max_length)

    updated_seq_x = []
    updated_seq_y = []

    pointer = 0
    while pointer < min_length:
        rand = random.uniform(0, 1)
        if rand <= 0.5:
            updated_seq_x += shortest[pointer:pointer + 1]
            updated_seq_y += longest[pointer:pointer + 1]
            pointer = pointer + 1
        else:
            updated_seq_x += longest[pointer:pointer + 1]
            updated_seq_y += shortest[pointer:pointer + 1]
            pointer = pointer + 1

    count = pointer
    while count < length_child_x:
        updated_seq_x += longest[pointer:pointer + 1]

    count = pointer
    while count < length_child_y:
        updated_seq_y += longest[pointer:pointer + 1]

    child_x = Program(updated_seq_x)
    child_y = Program(updated_seq_y)

    return child_x, child_y


# TODO: Uses n-point crossover for now, maybe change that?
def queen_bee_crossover(gen):
    i = 1
    queen = gen[0]

    children = []

    while i < len(gen):
        program = gen[i]
        child_x, child_y = n_point_crossover(queen, program)
        i += 1
        children.append(child_x)
        children.append(child_y)

    return children


def three_parent_crossover(gen):
    current_gen = copy.deepcopy(gen)
    N = len(gen)

    children = []

    for i in range(N):
        random.shuffle(current_gen)

        parent1 = current_gen[0]
        parent1_sequence = parent1.sequence
        length_parent1 = len(parent1_sequence)

        parent2 = current_gen[1]
        parent2_sequence = parent2.sequence
        length_parent2 = len(parent2_sequence)

        parent3 = current_gen[2]
        parent3_sequence = parent3.sequence
        length_parent3 = len(parent3_sequence)

        shortest = length_parent1
        longest = length_parent1

        if length_parent2 < shortest:
            shortest = length_parent2
        if length_parent2 > longest:
            longest = length_parent2

        if length_parent3 < shortest:
            shortest = length_parent3
        if length_parent3 > longest:
            longest = length_parent3

        length_child = random.randint(shortest, longest)
        child = []

        for j in range(length_child):
            if j < length_parent1 and j < length_parent2 and j < length_parent3:
                if parent1_sequence[j:j+1] == parent2_sequence[j:j+1]:
                    child += parent1_sequence[j:j+1]
                else:
                    child += parent3_sequence[j:j + 1]

            if j < length_parent1 and j < length_parent2 and j >= length_parent3:
                rand = random.uniform(0, 1)
                if rand <= 0.5:
                    child += parent1_sequence[j:j + 1]
                else:
                    child += parent2_sequence[j:j + 1]

            if j < length_parent1 and j >= length_parent2 and j < length_parent3:
                rand = random.uniform(0, 1)
                if rand <= 0.5:
                    child += parent1_sequence[j:j + 1]
                else:
                    child += parent3_sequence[j:j + 1]

            if j >= length_parent1 and j < length_parent2 and j < length_parent3:
                rand = random.uniform(0, 1)
                if rand <= 0.5:
                    child += parent2_sequence[j:j + 1]
                else:
                    child += parent3_sequence[j:j + 1]

            if j < length_parent1 and j >= length_parent2 and j >= length_parent3:
                child += parent1_sequence[j:j + 1]

            if j >= length_parent1 and j < length_parent2 and j >= length_parent3:
                child += parent2_sequence[j:j + 1]

            if j >= length_parent1 and j >= length_parent2 and j < length_parent3:
                child += parent3_sequence[j:j + 1]

        children.append(Program(child))

    return children


def add_occurrence(occurrences, gene):
    flag = False
    for (g, o) in occurrences:
        if g == gene:
            occurrences.remove((g, o))
            occurrences.append((gene, o + 1))
            flag = True
            break

    if not flag:
        occurrences.append((gene, 1))
    return occurrences


def multiple_parent_crossover(gen):
    current_gen = copy.deepcopy(gen)
    N = len(gen)
    k = 5

    children = []

    for i in range(N):
        random.shuffle(current_gen)

        parents_sequences = []
        parents_lengths = []
        for j in range(k):
            curr = current_gen[j].sequence
            parents_sequences.append(curr)
            parents_lengths.append(len(curr))
        shortest = min(parents_lengths)
        longest = max(parents_lengths)

        length_child = random.randint(shortest, longest)
        child = []

        for j in range(length_child):
            current_gen_occurrences = []
            for x in range(k):
                parent = parents_sequences[x]
                if j < len(parent):
                    occ = copy.deepcopy(current_gen_occurrences)
                    gene = parent[j:j + 1]
                    current_gen_occurrences = add_occurrence(current_gen_occurrences, gene)

            most = 0
            gene_most = None
            for (g, o) in current_gen_occurrences:
                if o > most:
                    most = o
                    gene_most = g
            child += gene_most

        children.append(Program(child))

    return children


# TODO: Check implementation
def random_cross_two_programs(program_x, program_y):
    program_x_sequence = program_x.sequence
    length_program_x = len(program_x_sequence)

    program_y_sequence = program_y.sequence
    length_program_y = len(program_y_sequence)

    shortest = min([length_program_x, length_program_y])
    longest = max([length_program_x, length_program_y])

    total_length = length_program_x + length_program_y
    child_length = random.randint(shortest, longest)

    # Randomize which parent goes starts first
    rand = random.uniform(0, 1)
    start_index_x  = 0
    start_index_y = 0
    end_index = 0
    if rand <= 0.5:
        start_index_y = random.randint(0, length_program_x)
        end_index = max((length_program_x - 1), (start_index_y + length_program_y - 1))
    else:
        start_index_x = random.randint(0, length_program_y)
        end_index = max((length_program_y - 1), (start_index_x + length_program_x - 1))

    start_index_child = random.randint(0, end_index - child_length + 1)

    child = []

    for i in range(child_length):
        index_child = i + start_index_child
        if start_index_x <= index_child < (start_index_x + length_program_x) and start_index_y <= index_child < (start_index_y + length_program_y):
            r = random.uniform(0, 1)
            if r <= 0.5:
                index = index_child - start_index_x
                child += program_x_sequence[index:index + 1]
            else:
                index = index_child - start_index_y
                child += program_y_sequence[index:index + 1]
        elif start_index_x <= index_child < (start_index_x + length_program_x):
            index = index_child - start_index_x
            child += program_x_sequence[index:index + 1]
        elif start_index_y <= index_child < (start_index_y + length_program_y):
            index = index_child - start_index_y
            child += program_y_sequence[index:index + 1]

    return Program(child)


def random_crossover(gen):
    N = len(gen)

    children = []
    for i in range(int(N/2)):
        program_x, program_y = gen[i], gen[i + 1]
        child = random_cross_two_programs(program_x, program_y)
        children.append(child)

    for i in range(int(N/2)):
        program_x, program_y = gen[i], gen[i + 1]
        child = random_cross_two_programs(program_x, program_y)
        children.append(child)

    return children

