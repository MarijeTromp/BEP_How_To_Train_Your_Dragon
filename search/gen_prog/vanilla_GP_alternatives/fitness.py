
import math
from common.tokens.abstract_tokens import InvalidTransition
from common.tokens.control_tokens import LoopIterationLimitReached

# ------------------------------------------------ Start original code ------------------------------------------------


def evaluate_program(program, training_examples):
    try:
        cum_loss = 0.0
        solved = True
        for example in training_examples:
            input = example.input_environment
            output = example.output_environment
            program_output = program.interp(input)
            cum_loss += program_output.distance(output)
            solved = solved and program_output.correct(output)
        if (solved):
            error = 0
            return (error, program)
        else:
            error = cum_loss
            # print(solved)
            return (error, program)
    except (InvalidTransition, LoopIterationLimitReached) as e:
        error = float("inf")
        return (error, program)


def gen_error(current_gen, training_examples):
    current_gen_error = []
    for program in current_gen:
        program_error = evaluate_program(program, training_examples)
        current_gen_error.append(program_error)
    current_gen_error = sorted(current_gen_error)

    return current_gen_error


def program_fitness(error):
    if (str(error) == "0" or math.isclose(error, 0, rel_tol=1e-05, abs_tol=1e-08)):
        return float("inf")
    elif (str(error) == "inf"):
        return 0
    else:
        return 1.0 / error


def gen_fitness(current_gen_error):
    current_gen_fitness = []
    for error, program in current_gen_error:
        fitness = program_fitness(error)
        current_gen_fitness.append((fitness, program))

    # Sort [(error, program)] by error decreasingly
    current_gen_fitness = sorted(current_gen_fitness, reverse=True)

    return current_gen_fitness

# ------------------------------------------------ End original code ------------------------------------------------


def program_error_example(program, example):
    try:
        loss = 0.0
        solved = True
        input_expected = example.input_environment
        output_expected = example.output_environment
        program_output = program.interp(input_expected)
        loss += program_output.distance(output_expected)
        solved = solved and program_output.correct(output_expected)
        if (solved):
            error = 0
            return error
        else:
            error = loss
            # print(solved)
            return error
    except (InvalidTransition, LoopIterationLimitReached) as e:
        error = float("inf")
        return error
