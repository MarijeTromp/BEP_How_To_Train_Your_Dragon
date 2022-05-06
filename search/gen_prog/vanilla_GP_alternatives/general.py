import math
import statistics
import random, itertools

# ------------------------------------------------ Start original code ------------------------------------------------

# Draw from a list of options randomly (no seed)
def draw_from(options, number_of_elems=0, weights=None):
    if (number_of_elems == 0):
        res = random.choices(options, weights=weights, k=1)[0]
        return res
    return random.choices(options, weights=weights, k=number_of_elems)


def normalize_fitness(current_gen_fitness):
    # Assumption: no negative errors
    inf_values, fin_values = [], []
    for err, _ in current_gen_fitness:
        if (math.isinf(err)):
            inf_values.append(err)
            continue
        fin_values.append(err)

    shift = 0
    max_fin_value = 0.5
    if (len(fin_values) != 0):
        max_fin_value = max(fin_values)

    if (math.isclose(max_fin_value, 0, rel_tol=1e-05, abs_tol=1e-08)):
        shift = 1
        max_fin_value += shift

    norm_errors = []
    sum = 0.0
    for err, program in current_gen_fitness:
        if (math.isinf(err)):
            inf_sub = max_fin_value * len(current_gen_fitness)
            norm_errors.append((inf_sub, program))
            sum += inf_sub
        else:
            shifted_error = err + shift
            norm_errors.append((shifted_error, program))
            sum += shifted_error

    error_prob = [(n_err / sum, program) for n_err, program in norm_errors]
    sorted(error_prob, reverse=True)
    return error_prob


def chose_with_prob(prob):
    return draw_from([True, False], weights=[prob, 1.0 - prob])


def pairs_from(items):
    n = 2
    args = [iter(items)] * n
    return itertools.zip_longest(*args)


def generation_stats(gen_fitness):
    prog_lengths = [p.number_of_tokens() for _, p in gen_fitness]
    prog_tokens = [len(p.sequence) for _, p in gen_fitness]
    std_dev_lengths = statistics.stdev(prog_lengths)
    std_dev_token = statistics.stdev(prog_tokens)
    print(std_dev_lengths, std_dev_token)
    print(statistics.mean(prog_lengths), statistics.mean(prog_tokens))


def roulette_wheel(gen_probabilities):
    wheel = []

    cum_probability = 0
    for probability, program in gen_probabilities:
        wheel.append((cum_probability, cum_probability + probability, program))
        cum_probability += probability

    return wheel


def select_on_wheel(wheel, pointer):
    # print("Wheel: ", wheel)
    try:
        for cum_probability, probability, program in wheel:
            if (cum_probability <= pointer and cum_probability + probability >= pointer):
                return program
        # print("Program not on the wheel: ", program, " pointer: ", pointer)
    except Exception as e:
        print("Something went wrong: pointer not on the wheel")


def select_N_on_wheel(wheel, N, stepsize, pointer):
    selected = []
    selected.append(select_on_wheel(wheel, pointer))
    for i in range(0, N - 1):
        pointer += stepsize
        pointer %= pointer
        selected.append(select_on_wheel(wheel, pointer))
    return selected

# ------------------------------------------------ End original code ------------------------------------------------
