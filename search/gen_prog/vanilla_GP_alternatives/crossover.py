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
        if rand < 0.5:
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
