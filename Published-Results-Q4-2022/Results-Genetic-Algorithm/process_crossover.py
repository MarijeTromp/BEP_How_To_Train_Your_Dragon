from fileinput import filename
import json
import sys
from collections import OrderedDict

from matplotlib import pyplot as plt


class ResultParser:
    def __init__(self, file):
        self.file = file

    def filter_result_fields(self, chosen_fields):
        results = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)
                filtered = []
                for f in chosen_fields:
                    if f in data:
                        filtered.append(data[f])
                results.append(filtered)
        return results

    def get_solved_count(self):
        solved, cases = 0, 0
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)
                if (data["train_cost"] == 0 and data["test_cost"] == 0):
                    solved += 1
                cases += 1
        return solved, cases

    def get_percentage_solved(self):
        solved, cases = self.get_solved_count()
        return str((solved / cases) * 100) + "%"

    def solved_percentage_by_complexity(self, domain):
        solved_percentage = {}

        if (domain == "robot"):
            solved_percentage = {"2": [0, 0], "4": [0, 0], "6": [0, 0], "8": [0, 0], "10": [0, 0]}
        elif (domain == "string"):
            solved_percentage = {"1": [0, 0], "2": [0, 0], "3": [0, 0], "4": [0, 0], "5": [0, 0], "6": [0, 0],
                                 "7": [0, 0], "8": [0, 0], "9": [0, 0]}
        else:
            solved_percentage = {"1": [0, 0], "2": [0, 0], "3": [0, 0], "4": [0, 0], "5": [0, 0]}

        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"][len(domain) + 2:]
                complexity = file_name.split('-')[0]

                if (data["train_cost"] == 0 and data["test_cost"] == 0):
                    solved_percentage[complexity][0] += 1
                solved_percentage[complexity][1] += 1

        for compl, (solved, total) in solved_percentage.items():
            if (total == 0):
                solved_percentage[compl] = 0
            else:
                solved_percentage[compl] = (solved / total) * 100

        return solved_percentage

    def avg_test_cost_by_complexity(self, domain):
        avg_test_cost = {}

        if (domain == "robot"):
            avg_test_cost = {"2": [0, 0], "4": [0, 0], "6": [0, 0], "8": [0, 0], "10": [0, 0]}
        elif (domain == "string"):
            avg_test_cost = {"1": [0, 0], "2": [0, 0], "3": [0, 0], "4": [0, 0], "5": [0, 0], "6": [0, 0],
                                 "7": [0, 0], "8": [0, 0], "9": [0, 0]}
        else:
            avg_test_cost = {"1": [0, 0], "2": [0, 0], "3": [0, 0], "4": [0, 0], "5": [0, 0]}

        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"][len(domain) + 2:]
                complexity = file_name.split('-')[0]

                # Skip infinite test cost, to not skew the data too much.
                if not (data["test_cost"] == float("inf")):
                    avg_test_cost[complexity][0] += data["test_cost"]
                    avg_test_cost[complexity][1] += 1

        for compl, (test_cost, total) in avg_test_cost.items():
            if (total == 0):
                avg_test_cost[compl] = 0
            else:
                avg_test_cost[compl] = (test_cost / total)

        return avg_test_cost

    def rel_improvement_by_complexity(self, domain):
        rel_improvement = {}

        if (domain == "robot"):
            rel_improvement = {"2": [0, 0], "4": [0, 0], "6": [0, 0], "8": [0, 0], "10": [0, 0]}
        elif (domain == "string"):
            rel_improvement = {"1": [0, 0], "2": [0, 0], "3": [0, 0], "4": [0, 0], "5": [0, 0], "6": [0, 0],
                               "7": [0, 0], "8": [0, 0], "9": [0, 0]}
        else:
            rel_improvement = {"1": [0, 0], "2": [0, 0], "3": [0, 0], "4": [0, 0], "5": [0, 0]}

        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"][len(domain) + 2:]
                complexity = file_name.split('-')[0]

                initial_error = data["initial_error"]
                final_cost = data["train_cost"]

                if (initial_error == 0):
                    percentage_imp = 1
                else:
                    percentage_imp = (initial_error - final_cost) / initial_error

                rel_improvement[complexity][0] += percentage_imp
                rel_improvement[complexity][1] += 1

        for compl, [percent_sum, total_num] in rel_improvement.items():
            if (total_num == 0):
                rel_improvement[compl] = 0
            else:
                rel_improvement[compl] = (percent_sum / total_num) * 100

        return rel_improvement

    #####################

    def get_solved_count_by_complexity(self, domain):
        solved_count = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"][len(domain) + 2:]
                complexity = file_name.split('-')[0]

                if (data["train_cost"] == 0 and data["test_cost"] == 0):
                    solved_count.append((complexity, 1))

        solved_by_complexity = OrderedDict()
        for k, *v in solved_count:
            solved_by_complexity.setdefault(k, []).append(v)

        complexity_list = list(solved_by_complexity.items())
        solved_by_complexity = [(c, sum(sum(l_s, []))) for (c, l_s) in complexity_list]

        return solved_by_complexity

    def get_initial_error(self, example_name):
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"]

                if (file_name == example_name):
                    initial_error = data["initial_error"]
                    return initial_error

    def relative_improvement(self):
        rel_improvement_all_files = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"]

                initial_error = data["initial_error"]
                final_cost = data["train_cost"]
                if (initial_error == 0):
                    rel_improvement = 100.0
                else:
                    rel_improvement = ((initial_error - final_cost) / initial_error) * 100.0
                rel_improvement_all_files.append((file_name, rel_improvement))
        return rel_improvement_all_files

    def get_train_vs_test_cost(self):
        return self.filter_result_fields(["train_cost", "test_cost"])

    def error_progression(self, example_name):
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                if (data["file"] == example_name):
                    costs_per_iteration = data["cost_per_iteration"]
                    return costs_per_iteration


# Initialization
# OnePoint
gp_path_to_file_pixel_OnePoint = "../../../../results/pixel/OnePoint.txt"
gp_path_to_file_robot_OnePoint = "../../../../results/robot/OnePoint.txt"
gp_path_to_file_string_OnePoint = "../../../../results/string/OnePoint.txt"

gp_result_parser_pixel_OnePoint = ResultParser(gp_path_to_file_pixel_OnePoint)
gp_result_parser_robot_OnePoint = ResultParser(gp_path_to_file_robot_OnePoint)
gp_result_parser_string_OnePoint = ResultParser(gp_path_to_file_string_OnePoint)

# NPoint
gp_path_to_file_pixel_NPoint = "../../../../results/pixel/NPoint.txt"
gp_path_to_file_robot_NPoint = "../../../../results/robot/NPoint.txt"
gp_path_to_file_string_NPoint = "../../../../results/string/NPoint.txt"

gp_result_parser_pixel_NPoint = ResultParser(gp_path_to_file_pixel_NPoint)
gp_result_parser_robot_NPoint = ResultParser(gp_path_to_file_robot_NPoint)
gp_result_parser_string_NPoint = ResultParser(gp_path_to_file_string_NPoint)

# TwoPoint
gp_path_to_file_pixel_TwoPoint = "../../../../results/pixel/TwoPoint.txt"
gp_path_to_file_robot_TwoPoint = "../../../../results/robot/TwoPoint.txt"
gp_path_to_file_string_TwoPoint = "../../../../results/string/TwoPoint.txt"

gp_result_parser_pixel_TwoPoint = ResultParser(gp_path_to_file_pixel_TwoPoint)
gp_result_parser_robot_TwoPoint = ResultParser(gp_path_to_file_robot_TwoPoint)
gp_result_parser_string_TwoPoint = ResultParser(gp_path_to_file_string_TwoPoint)

# Uniform
gp_path_to_file_pixel_Uniform = "../../../../results/pixel/Uniform.txt"
gp_path_to_file_robot_Uniform = "../../../../results/robot/Uniform.txt"
gp_path_to_file_string_Uniform = "../../../../results/string/Uniform.txt"

gp_result_parser_pixel_Uniform = ResultParser(gp_path_to_file_pixel_Uniform)
gp_result_parser_robot_Uniform = ResultParser(gp_path_to_file_robot_Uniform)
gp_result_parser_string_Uniform = ResultParser(gp_path_to_file_string_Uniform)

# QueenBee
gp_path_to_file_pixel_QueenBee = "../../../../results/pixel/QueenBee.txt"
gp_path_to_file_robot_QueenBee = "../../../../results/robot/QueenBee.txt"
gp_path_to_file_string_QueenBee = "../../../../results/string/QueenBee.txt"

gp_result_parser_pixel_QueenBee = ResultParser(gp_path_to_file_pixel_QueenBee)
gp_result_parser_robot_QueenBee = ResultParser(gp_path_to_file_robot_QueenBee)
gp_result_parser_string_QueenBee = ResultParser(gp_path_to_file_string_QueenBee)

# ThreeParent
gp_path_to_file_pixel_ThreeParent = "../../../../results/pixel/ThreeParent.txt"
gp_path_to_file_robot_ThreeParent = "../../../../results/robot/ThreeParent.txt"
gp_path_to_file_string_ThreeParent = "../../../../results/string/ThreeParent.txt"

gp_result_parser_pixel_ThreeParent = ResultParser(gp_path_to_file_pixel_ThreeParent)
gp_result_parser_robot_ThreeParent = ResultParser(gp_path_to_file_robot_ThreeParent)
gp_result_parser_string_ThreeParent = ResultParser(gp_path_to_file_string_ThreeParent)

# MultipleParent
gp_path_to_file_pixel_MultipleParent = "../../../../results/pixel/MultipleParent.txt"
gp_path_to_file_robot_MultipleParent = "../../../../results/robot/MultipleParent.txt"
gp_path_to_file_string_MultipleParent = "../../../../results/string/MultipleParent.txt"

gp_result_parser_pixel_MultipleParent = ResultParser(gp_path_to_file_pixel_MultipleParent)
gp_result_parser_robot_MultipleParent = ResultParser(gp_path_to_file_robot_MultipleParent)
gp_result_parser_string_MultipleParent = ResultParser(gp_path_to_file_string_MultipleParent)

# Random
gp_path_to_file_pixel_Random = "../../../../results/pixel/Random.txt"
gp_path_to_file_robot_Random = "../../../../results/robot/Random.txt"
gp_path_to_file_string_Random = "../../../../results/string/Random.txt"

gp_result_parser_pixel_Random = ResultParser(gp_path_to_file_pixel_Random)
gp_result_parser_robot_Random = ResultParser(gp_path_to_file_robot_Random)
gp_result_parser_string_Random = ResultParser(gp_path_to_file_string_Random)


def plot_error_progression(domain, example_name):
    initial_error = 0.0

    gp_cost_per_iteration_NPoint = []
    if (domain == "pixel"):
        initial_error = gp_result_parser_pixel_NPoint.get_initial_error(example_name)
        gp_cost_per_iteration_NPoint = gp_result_parser_pixel_NPoint.error_progression(example_name)
    elif (domain == "robot"):
        initial_error = gp_result_parser_robot_NPoint.get_initial_error(example_name)
        gp_cost_per_iteration_NPoint = gp_result_parser_robot_NPoint.error_progression(example_name)
    elif (domain == "string"):
        initial_error = gp_result_parser_string_NPoint.get_initial_error(example_name)
        gp_cost_per_iteration_NPoint = gp_result_parser_string_NPoint.error_progression(example_name)

    initial_error_line = [(i, initial_error) for i in [*range(0, len(gp_cost_per_iteration_NPoint))]]

    gp_cost_per_iteration_OnePoint = []
    if (domain == "pixel"):
        gp_cost_per_iteration_OnePoint = gp_result_parser_pixel_OnePoint.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_OnePoint = gp_result_parser_robot_OnePoint.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_OnePoint = gp_result_parser_string_OnePoint.error_progression(example_name)

    gp_cost_per_iteration_TwoPoint = []
    if (domain == "pixel"):
        gp_cost_per_iteration_TwoPoint = gp_result_parser_pixel_TwoPoint.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_TwoPoint = gp_result_parser_robot_TwoPoint.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_TwoPoint= gp_result_parser_string_TwoPoint.error_progression(example_name)

    gp_cost_per_iteration_Uniform = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Uniform = gp_result_parser_pixel_Uniform.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Uniform = gp_result_parser_robot_Uniform.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Uniform = gp_result_parser_string_Uniform.error_progression(example_name)

    gp_cost_per_iteration_QueenBee = []
    if (domain == "pixel"):
        gp_cost_per_iteration_QueenBee = gp_result_parser_pixel_QueenBee.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_QueenBee = gp_result_parser_robot_QueenBee.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_QueenBee = gp_result_parser_string_QueenBee.error_progression(example_name)

    gp_cost_per_iteration_ThreeParent = []
    if (domain == "pixel"):
        gp_cost_per_iteration_ThreeParent = gp_result_parser_pixel_ThreeParent.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_ThreeParent = gp_result_parser_robot_ThreeParent.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_ThreeParent = gp_result_parser_string_ThreeParent.error_progression(example_name)

    gp_cost_per_iteration_MultipleParent = []
    if (domain == "pixel"):
        gp_cost_per_iteration_MultipleParent = gp_result_parser_pixel_MultipleParent.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_MultipleParent = gp_result_parser_robot_MultipleParent.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_MultipleParent = gp_result_parser_string_MultipleParent.error_progression(example_name)

    gp_cost_per_iteration_Random = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Random = gp_result_parser_pixel_Random.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Random = gp_result_parser_robot_Random.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Random = gp_result_parser_string_Random.error_progression(example_name)

    fig, ax = plt.subplots()
    ax.plot(*zip(*gp_cost_per_iteration_OnePoint), label="Original NPoint", color="midnightBlue")
    ax.plot(*zip(*gp_cost_per_iteration_NPoint), label="NPoint", color="mediumseagreen")
    ax.plot(*zip(*gp_cost_per_iteration_TwoPoint), label="Two-Point", color="mediumpurple")
    ax.plot(*zip(*gp_cost_per_iteration_Uniform), label="Uniform", color="orangered")
    ax.plot(*zip(*gp_cost_per_iteration_QueenBee), label="Queen Bee", color="gold")
    ax.plot(*zip(*gp_cost_per_iteration_ThreeParent), label="Three Parent", color="slategrey")
    ax.plot(*zip(*gp_cost_per_iteration_MultipleParent), label="Multiple Parent", color="deepPink")
    ax.plot(*zip(*gp_cost_per_iteration_Random), label="Random", color="peru")
    ax.plot(*zip(*initial_error_line), label="Initial Error", color="black")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Error")
    ax.legend()
    ax.set_title("Error Progression in Example {}".format(example_name))

    plt.savefig("plots/error_progression_crossover.svg")
    fig.clf()
    plt.close


def plot_complexity_vs_solved_percentage():
    #fig, (ax2, ax3) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

    # Pixel
    domain = "pixel"
    gp_solved_percentage_OnePoint = gp_result_parser_pixel_OnePoint.solved_percentage_by_complexity(domain)
    gp_solved_percentage_NPoint = gp_result_parser_pixel_NPoint.solved_percentage_by_complexity(domain)
    gp_solved_percentage_TwoPoint = gp_result_parser_pixel_TwoPoint.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Uniform = gp_result_parser_pixel_Uniform.solved_percentage_by_complexity(domain)
    gp_solved_percentage_QueenBee = gp_result_parser_pixel_QueenBee.solved_percentage_by_complexity(domain)
    gp_solved_percentage_ThreeParent = gp_result_parser_pixel_ThreeParent.solved_percentage_by_complexity(domain)
    gp_solved_percentage_MultipleParent = gp_result_parser_pixel_MultipleParent.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Random = gp_result_parser_pixel_Random.solved_percentage_by_complexity(domain)

    ax1.plot(gp_solved_percentage_OnePoint.keys(), gp_solved_percentage_OnePoint.values(), label="One-Point", color="midnightBlue", marker="o")
    ax1.plot(gp_solved_percentage_NPoint.keys(), gp_solved_percentage_NPoint.values(), label="NPoint", color="mediumseagreen", marker="^")
    ax1.plot(gp_solved_percentage_TwoPoint.keys(), gp_solved_percentage_TwoPoint.values(), label="Two-Point", color="mediumpurple", marker="o")
    ax1.plot(gp_solved_percentage_Uniform.keys(), gp_solved_percentage_Uniform.values(), label="Uniform", color="orangered", marker="^")
    ax1.plot(gp_solved_percentage_QueenBee.keys(), gp_solved_percentage_QueenBee.values(), label="Queen Bee", color="gold", marker="o")
    ax1.plot(gp_solved_percentage_ThreeParent.keys(), gp_solved_percentage_ThreeParent.values(), label="Three Parent", color="slategrey", marker="^")
    ax1.plot(gp_solved_percentage_MultipleParent.keys(), gp_solved_percentage_MultipleParent.values(), label="Multiple Parent", color="deepPink", marker="o")
    ax1.plot(gp_solved_percentage_Random.keys(), gp_solved_percentage_Random.values(), label="Random", color="peru", marker="^")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Tasks Solved (%)")
    ax1.legend()
    ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_solved_percentage_OnePoint = gp_result_parser_robot_OnePoint.solved_percentage_by_complexity(domain)
    gp_solved_percentage_NPoint = gp_result_parser_robot_NPoint.solved_percentage_by_complexity(domain)
    gp_solved_percentage_TwoPoint = gp_result_parser_robot_TwoPoint.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Uniform = gp_result_parser_robot_Uniform.solved_percentage_by_complexity(domain)
    gp_solved_percentage_QueenBee = gp_result_parser_robot_QueenBee.solved_percentage_by_complexity(domain)
    gp_solved_percentage_ThreeParent = gp_result_parser_robot_ThreeParent.solved_percentage_by_complexity(domain)
    gp_solved_percentage_MultipleParent = gp_result_parser_robot_MultipleParent.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Random = gp_result_parser_robot_Random.solved_percentage_by_complexity(domain)

    ax2.plot(gp_solved_percentage_OnePoint.keys(), gp_solved_percentage_OnePoint.values(), label="One-Point", color="midnightBlue", marker="o")
    ax2.plot(gp_solved_percentage_NPoint.keys(), gp_solved_percentage_NPoint.values(), label="N-Point", color="mediumseagreen", marker="^")
    ax2.plot(gp_solved_percentage_TwoPoint.keys(), gp_solved_percentage_TwoPoint.values(), label="Two-Point", color="mediumpurple", marker="o")
    ax2.plot(gp_solved_percentage_Uniform.keys(), gp_solved_percentage_Uniform.values(), label="Uniform", color="orangered", marker="^")
    ax2.plot(gp_solved_percentage_QueenBee.keys(), gp_solved_percentage_QueenBee.values(), label="Queen Bee", color="gold", marker="o")
    ax2.plot(gp_solved_percentage_ThreeParent.keys(), gp_solved_percentage_ThreeParent.values(), label="Three Parent", color="slategrey", marker="^")
    ax2.plot(gp_solved_percentage_MultipleParent.keys(), gp_solved_percentage_MultipleParent.values(), label="Multiple Parent", color="deepPink", marker="o")
    ax2.plot(gp_solved_percentage_Random.keys(), gp_solved_percentage_Random.values(), label="Random", color="peru", marker="^")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Tasks Solved (%)")
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_solved_percentage_OnePoint = gp_result_parser_string_OnePoint.solved_percentage_by_complexity(domain)
    gp_solved_percentage_NPoint = gp_result_parser_string_NPoint.solved_percentage_by_complexity(domain)
    gp_solved_percentage_TwoPoint = gp_result_parser_string_TwoPoint.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Uniform = gp_result_parser_string_Uniform.solved_percentage_by_complexity(domain)
    gp_solved_percentage_QueenBee = gp_result_parser_string_QueenBee.solved_percentage_by_complexity(domain)
    gp_solved_percentage_ThreeParent = gp_result_parser_string_ThreeParent.solved_percentage_by_complexity(domain)
    gp_solved_percentage_MultipleParent = gp_result_parser_string_MultipleParent.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Random = gp_result_parser_string_Random.solved_percentage_by_complexity(domain)

    ax3.plot(gp_solved_percentage_OnePoint.keys(), gp_solved_percentage_OnePoint.values(), label="One-Point", color="midnightBlue", marker="o")
    ax3.plot(gp_solved_percentage_NPoint.keys(), gp_solved_percentage_NPoint.values(), label="N-Point", color="mediumseagreen", marker="^")
    ax3.plot(gp_solved_percentage_TwoPoint.keys(), gp_solved_percentage_TwoPoint.values(), label="Two-Point", color="mediumpurple", marker="o")
    ax3.plot(gp_solved_percentage_Uniform.keys(), gp_solved_percentage_Uniform.values(), label="Uniform", color="orangered", marker="^")
    ax3.plot(gp_solved_percentage_QueenBee.keys(), gp_solved_percentage_QueenBee.values(), label="Queen Bee", color="gold", marker="o")
    ax3.plot(gp_solved_percentage_ThreeParent.keys(), gp_solved_percentage_ThreeParent.values(), label="Three Parent", color="slategrey", marker="^")
    ax3.plot(gp_solved_percentage_MultipleParent.keys(), gp_solved_percentage_MultipleParent.values(), label="Multiple Parent", color="deepPink", marker="o")
    ax3.plot(gp_solved_percentage_Random.keys(), gp_solved_percentage_Random.values(), label="Random", color="peru", marker="^")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Tasks Solved (%)")
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/solved_percentage_crossover.svg")
    fig.clf()
    plt.close

def plot_complexity_vs_avg_test_cost():
    fig, (ax2, ax3) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    #fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

    # Pixel
    domain = "pixel"
    gp_avg_test_cost_OnePoint = gp_result_parser_pixel_OnePoint.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_NPoint = gp_result_parser_pixel_NPoint.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_TwoPoint = gp_result_parser_pixel_TwoPoint.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Uniform = gp_result_parser_pixel_Uniform.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_QueenBee = gp_result_parser_pixel_QueenBee.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_ThreeParent = gp_result_parser_pixel_ThreeParent.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_MultipleParent = gp_result_parser_pixel_MultipleParent.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Random = gp_result_parser_pixel_Random.avg_test_cost_by_complexity(domain)

    #ax1.plot(gp_avg_test_cost_OnePoint.keys(), gp_avg_test_cost_OnePoint.values(), label="One-Point", color="midnightBlue", marker="o")
    #ax1.plot(gp_avg_test_cost_NPoint.keys(), gp_avg_test_cost_NPoint.values(), label="N-Point", color="mediumseagreen", marker="^")
    #ax1.plot(gp_avg_test_cost_TwoPoint.keys(), gp_avg_test_cost_TwoPoint.values(), label="Two-Point", color="mediumpurple", marker="o")
    #ax1.plot(gp_avg_test_cost_Uniform.keys(), gp_avg_test_cost_Uniform.values(), label="Uniform", color="orangered", marker="^")
    #ax1.plot(gp_avg_test_cost_QueenBee.keys(), gp_avg_test_cost_QueenBee.values(), label="Queen Bee", color="gold", marker="o")
    #ax1.plot(gp_avg_test_cost_ThreeParent.keys(), gp_avg_test_cost_ThreeParent.values(), label="Three Parent", color="slategrey", marker="^")
    #ax1.plot(gp_avg_test_cost_MultipleParent.keys(), gp_avg_test_cost_MultipleParent.values(), label="Multiple Parent", color="deepPink", marker="o")
    #ax1.plot(gp_avg_test_cost_Random.keys(), gp_avg_test_cost_Random.values(), label="Random", color="peru", marker="^")
    #ax1.set_xlabel("Task Complexity")
    #ax1.set_ylabel("Average Test-Cost")
    #ax1.legend()
    #ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_avg_test_cost_OnePoint = gp_result_parser_robot_OnePoint.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_NPoint = gp_result_parser_robot_NPoint.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_TwoPoint = gp_result_parser_robot_TwoPoint.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Uniform = gp_result_parser_robot_Uniform.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_QueenBee = gp_result_parser_robot_QueenBee.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_ThreeParent = gp_result_parser_robot_ThreeParent.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_MultipleParent = gp_result_parser_robot_MultipleParent.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Random = gp_result_parser_robot_Random.avg_test_cost_by_complexity(domain)

    ax2.plot(gp_avg_test_cost_OnePoint.keys(), gp_avg_test_cost_OnePoint.values(), label="One Point", color="midnightBlue", marker="o")
    ax2.plot(gp_avg_test_cost_NPoint.keys(), gp_avg_test_cost_NPoint.values(), label="N-Point", color="mediumseagreen", marker="^")
    ax2.plot(gp_avg_test_cost_TwoPoint.keys(), gp_avg_test_cost_TwoPoint.values(), label="Two-Point", color="mediumpurple", marker="o")
    ax2.plot(gp_avg_test_cost_Uniform.keys(), gp_avg_test_cost_Uniform.values(), label="Uniform", color="orangered", marker="^")
    ax2.plot(gp_avg_test_cost_QueenBee.keys(), gp_avg_test_cost_QueenBee.values(), label="Queen Bee", color="gold", marker="o")
    ax2.plot(gp_avg_test_cost_ThreeParent.keys(), gp_avg_test_cost_ThreeParent.values(), label="Three Parent", color="slategrey", marker="^")
    ax2.plot(gp_avg_test_cost_MultipleParent.keys(), gp_avg_test_cost_MultipleParent.values(), label="Multiple Parent", color="deepPink", marker="o")
    ax2.plot(gp_avg_test_cost_Random.keys(), gp_avg_test_cost_Random.values(), label="Random", color="peru", marker="^")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Average Test-Cost")
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_avg_test_cost_OnePoint = gp_result_parser_string_OnePoint.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_NPoint = gp_result_parser_string_NPoint.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_TwoPoint = gp_result_parser_string_TwoPoint.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Uniform = gp_result_parser_string_Uniform.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_QueenBee = gp_result_parser_string_QueenBee.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_ThreeParent = gp_result_parser_string_ThreeParent.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_MultipleParent = gp_result_parser_string_MultipleParent.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Random = gp_result_parser_string_Random.avg_test_cost_by_complexity(domain)

    ax3.plot(gp_avg_test_cost_OnePoint.keys(), gp_avg_test_cost_OnePoint.values(), label="One Point", color="midnightBlue", marker="o")
    ax3.plot(gp_avg_test_cost_NPoint.keys(), gp_avg_test_cost_NPoint.values(), label="N-Point", color="mediumseagreen", marker="^")
    ax3.plot(gp_avg_test_cost_TwoPoint.keys(), gp_avg_test_cost_TwoPoint.values(), label="Two-Point", color="mediumpurple", marker="o")
    ax3.plot(gp_avg_test_cost_Uniform.keys(), gp_avg_test_cost_Uniform.values(), label="Uniform", color="orangered", marker="^")
    ax3.plot(gp_avg_test_cost_QueenBee.keys(), gp_avg_test_cost_QueenBee.values(), label="Queen Bee", color="gold", marker="o")
    ax3.plot(gp_avg_test_cost_ThreeParent.keys(), gp_avg_test_cost_ThreeParent.values(), label="Three Parent", color="slategrey", marker="^")
    ax3.plot(gp_avg_test_cost_MultipleParent.keys(), gp_avg_test_cost_MultipleParent.values(), label="Multiple Parent", color="deepPink", marker="o")
    ax3.plot(gp_avg_test_cost_Random.keys(), gp_avg_test_cost_Random.values(), label="Random", color="peru", marker="^")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Average Test-Cost")
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/avg_test_cost_crossover.svg")
    fig.clf()
    plt.close

def plot_rel_improvement():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

    # Pixel
    domain = "pixel"
    gp_avg_rel_improvement_OnePoint = gp_result_parser_pixel_OnePoint.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_NPoint = gp_result_parser_pixel_NPoint.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_TwoPoint = gp_result_parser_pixel_TwoPoint.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Uniform = gp_result_parser_pixel_Uniform.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_QueenBee = gp_result_parser_pixel_QueenBee.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_ThreeParent = gp_result_parser_pixel_ThreeParent.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_MultipleParent = gp_result_parser_pixel_MultipleParent.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Random = gp_result_parser_pixel_Random.rel_improvement_by_complexity(domain)

    ax1.plot(gp_avg_rel_improvement_OnePoint.keys(), gp_avg_rel_improvement_OnePoint.values(), label="One-Point", color="midnightBlue",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_NPoint.keys(), gp_avg_rel_improvement_NPoint.values(), label="NPoint", color="mediumseagreen",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_TwoPoint.keys(), gp_avg_rel_improvement_TwoPoint.values(), label="Two-Point",
             color="mediumpurple",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_Uniform.keys(), gp_avg_rel_improvement_Uniform.values(), label="Uniform",
             color="orangered",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_QueenBee.keys(), gp_avg_rel_improvement_QueenBee.values(), label="Queen Bee",
             color="gold",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_ThreeParent.keys(), gp_avg_rel_improvement_ThreeParent.values(), label="Three Parent",
             color="slategrey",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_MultipleParent.keys(), gp_avg_rel_improvement_MultipleParent.values(), label="Multiple Parent",
             color="deepPink",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_Random.keys(), gp_avg_rel_improvement_Random.values(), label="Random",
             color="peru",
             marker="^")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Avg. Relative Improvement (%)")
    ax1.set_ylim(ymin=0)
    ax1.legend()
    ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_avg_rel_improvement_OnePoint = gp_result_parser_robot_OnePoint.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_NPoint = gp_result_parser_robot_NPoint.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_TwoPoint = gp_result_parser_robot_TwoPoint.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Uniform = gp_result_parser_robot_Uniform.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_QueenBee = gp_result_parser_robot_QueenBee.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_ThreeParent = gp_result_parser_robot_ThreeParent.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_MultipleParent = gp_result_parser_robot_MultipleParent.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Random = gp_result_parser_robot_Random.rel_improvement_by_complexity(domain)

    ax2.plot(gp_avg_rel_improvement_OnePoint.keys(), gp_avg_rel_improvement_OnePoint.values(), label="One-Point", color="midnightBlue",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_NPoint.keys(), gp_avg_rel_improvement_NPoint.values(), label="N-Point", color="mediumseagreen",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_TwoPoint.keys(), gp_avg_rel_improvement_TwoPoint.values(), label="Two-Point",
             color="mediumpurple",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_Uniform.keys(), gp_avg_rel_improvement_Uniform.values(), label="Uniform",
             color="orangered",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_QueenBee.keys(), gp_avg_rel_improvement_QueenBee.values(), label="Queen Bee",
             color="gold",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_ThreeParent.keys(), gp_avg_rel_improvement_ThreeParent.values(), label="Three Parent",
             color="slategrey",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_MultipleParent.keys(), gp_avg_rel_improvement_MultipleParent.values(), label="Multiple Parent",
             color="deepPink",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_Random.keys(), gp_avg_rel_improvement_Random.values(), label="Random",
             color="peru",
             marker="^")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Avg. Relative Improvement (%)")
    ax2.set_ylim(ymin=0)
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_avg_rel_improvement_OnePoint = gp_result_parser_string_OnePoint.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_NPoint = gp_result_parser_string_NPoint.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_TwoPoint = gp_result_parser_string_TwoPoint.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Uniform = gp_result_parser_string_Uniform.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_QueenBee = gp_result_parser_string_QueenBee.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_ThreeParent = gp_result_parser_string_ThreeParent.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_MultipleParent = gp_result_parser_string_MultipleParent.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Random = gp_result_parser_string_Random.rel_improvement_by_complexity(domain)

    ax3.plot(gp_avg_rel_improvement_OnePoint.keys(), gp_avg_rel_improvement_OnePoint.values(), label="One-Point", color="midnightBlue",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_NPoint.keys(), gp_avg_rel_improvement_NPoint.values(), label="N-Point", color="mediumseagreen",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_TwoPoint.keys(), gp_avg_rel_improvement_TwoPoint.values(), label="TwoPoint",
             color="mediumpurple",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_Uniform.keys(), gp_avg_rel_improvement_Uniform.values(), label="Uniform",
             color="orangered",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_QueenBee.keys(), gp_avg_rel_improvement_QueenBee.values(), label="Queen Bee",
             color="gold",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_ThreeParent.keys(), gp_avg_rel_improvement_ThreeParent.values(), label="Three Parent",
             color="slategrey",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_MultipleParent.keys(), gp_avg_rel_improvement_MultipleParent.values(), label="Multiple Parent",
             color="deepPink",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_Random.keys(), gp_avg_rel_improvement_Random.values(), label="Random",
             color="peru",
             marker="^")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Avg. Relative Improvement (%)")
    ax3.set_ylim(ymin=0)
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/relative_improvement_crossover.svg")
    fig.clf()
    plt.close

def plot_dis_to_correct():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

plot_rel_improvement()
plot_complexity_vs_solved_percentage()
plot_error_progression("string", "strings/1-58-1.pl")
plot_complexity_vs_avg_test_cost()
