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
# Classical
gp_path_to_file_pixel_Classical = "../../../../results/pixel/Classical.txt"
gp_path_to_file_robot_Classical = "../../../../results/robot/Classical.txt"
gp_path_to_file_string_Classical = "../../../../results/string/Classical.txt"

gp_result_parser_pixel_Classical = ResultParser(gp_path_to_file_pixel_Classical)
gp_result_parser_robot_Classical = ResultParser(gp_path_to_file_robot_Classical)
gp_result_parser_string_Classical = ResultParser(gp_path_to_file_string_Classical)

# UMAD
gp_path_to_file_pixel_UMAD = "../../../../results/pixel/UMAD.txt"
gp_path_to_file_robot_UMAD = "../../../../results/robot/UMAD.txt"
gp_path_to_file_string_UMAD = "../../../../results/string/UMAD.txt"

gp_result_parser_pixel_UMAD = ResultParser(gp_path_to_file_pixel_UMAD)
gp_result_parser_robot_UMAD = ResultParser(gp_path_to_file_robot_UMAD)
gp_result_parser_string_UMAD = ResultParser(gp_path_to_file_string_UMAD)

# OneMutation
gp_path_to_file_pixel_OneMutation = "../../../../results/pixel/OneMutation.txt"
gp_path_to_file_robot_OneMutation = "../../../../results/robot/OneMutation.txt"
gp_path_to_file_string_OneMutation = "../../../../results/string/OneMutation.txt"

gp_result_parser_pixel_OneMutation = ResultParser(gp_path_to_file_pixel_OneMutation)
gp_result_parser_robot_OneMutation = ResultParser(gp_path_to_file_robot_OneMutation)
gp_result_parser_string_OneMutation = ResultParser(gp_path_to_file_string_OneMutation)

# AlteredOneMutation
gp_path_to_file_pixel_AlteredOneMutation = "../../../../results/pixel/AlteredOneMutation.txt"
gp_path_to_file_robot_AlteredOneMutation = "../../../../results/robot/AlteredOneMutation.txt"
gp_path_to_file_string_AlteredOneMutation = "../../../../results/string/AlteredOneMutation.txt"

gp_result_parser_pixel_AlteredOneMutation = ResultParser(gp_path_to_file_pixel_AlteredOneMutation)
gp_result_parser_robot_AlteredOneMutation = ResultParser(gp_path_to_file_robot_AlteredOneMutation)
gp_result_parser_string_AlteredOneMutation = ResultParser(gp_path_to_file_string_AlteredOneMutation)

# Interchanging
gp_path_to_file_pixel_Interchanging = "../../../../results/pixel/Interchanging.txt"
gp_path_to_file_robot_Interchanging = "../../../../results/robot/Interchanging.txt"
gp_path_to_file_string_Interchanging = "../../../../results/string/Interchanging.txt"

gp_result_parser_pixel_Interchanging = ResultParser(gp_path_to_file_pixel_Interchanging)
gp_result_parser_robot_Interchanging = ResultParser(gp_path_to_file_robot_Interchanging)
gp_result_parser_string_Interchanging = ResultParser(gp_path_to_file_string_Interchanging)

# Scramble
gp_path_to_file_pixel_Scramble = "../../../../results/pixel/Scramble.txt"
gp_path_to_file_robot_Scramble = "../../../../results/robot/Scramble.txt"
gp_path_to_file_string_Scramble = "../../../../results/string/Scramble.txt"

gp_result_parser_pixel_Scramble = ResultParser(gp_path_to_file_pixel_Scramble)
gp_result_parser_robot_Scramble = ResultParser(gp_path_to_file_robot_Scramble)
gp_result_parser_string_Scramble = ResultParser(gp_path_to_file_string_Scramble)

# Reversing
gp_path_to_file_pixel_Reversing = "../../../../results/pixel/Reversing.txt"
gp_path_to_file_robot_Reversing = "../../../../results/robot/Reversing.txt"
gp_path_to_file_string_Reversing = "../../../../results/string/Reversing.txt"

gp_result_parser_pixel_Reversing = ResultParser(gp_path_to_file_pixel_Reversing)
gp_result_parser_robot_Reversing = ResultParser(gp_path_to_file_robot_Reversing)
gp_result_parser_string_Reversing = ResultParser(gp_path_to_file_string_Reversing)

def plot_error_progression(domain, example_name):
    initial_error = 0.0

    gp_cost_per_iteration_UMAD = []
    if (domain == "pixel"):
        initial_error = gp_result_parser_pixel_UMAD.get_initial_error(example_name)
        gp_cost_per_iteration_UMAD = gp_result_parser_pixel_UMAD.error_progression(example_name)
    elif (domain == "robot"):
        initial_error = gp_result_parser_robot_UMAD.get_initial_error(example_name)
        gp_cost_per_iteration_UMAD = gp_result_parser_robot_UMAD.error_progression(example_name)
    elif (domain == "string"):
        initial_error = gp_result_parser_string_UMAD.get_initial_error(example_name)
        gp_cost_per_iteration_UMAD = gp_result_parser_string_UMAD.error_progression(example_name)

    initial_error_line = [(i, initial_error) for i in [*range(0, len(gp_cost_per_iteration_UMAD))]]

    gp_cost_per_iteration_Classical = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Classical = gp_result_parser_pixel_Classical.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Classical = gp_result_parser_robot_Classical.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Classical = gp_result_parser_string_Classical.error_progression(example_name)

    gp_cost_per_iteration_OneMutation = []
    if (domain == "pixel"):
        gp_cost_per_iteration_OneMutation = gp_result_parser_pixel_OneMutation.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_OneMutation = gp_result_parser_robot_OneMutation.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_OneMutation= gp_result_parser_string_OneMutation.error_progression(example_name)

    gp_cost_per_iteration_AlteredOneMutation = []
    if (domain == "pixel"):
        gp_cost_per_iteration_AlteredOneMutation = gp_result_parser_pixel_AlteredOneMutation.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_AlteredOneMutation = gp_result_parser_robot_AlteredOneMutation.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_AlteredOneMutation = gp_result_parser_string_AlteredOneMutation.error_progression(example_name)

    gp_cost_per_iteration_Interchanging = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Interchanging = gp_result_parser_pixel_Interchanging.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Interchanging = gp_result_parser_robot_Interchanging.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Interchanging = gp_result_parser_string_Interchanging.error_progression(example_name)

    gp_cost_per_iteration_Scramble = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Scramble = gp_result_parser_pixel_Scramble.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Scramble = gp_result_parser_robot_Scramble.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Scramble = gp_result_parser_string_Scramble.error_progression(example_name)

    gp_cost_per_iteration_Reversing = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Reversing = gp_result_parser_pixel_Reversing.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Reversing = gp_result_parser_robot_Reversing.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Reversing = gp_result_parser_string_Reversing.error_progression(example_name)

    fig, ax = plt.subplots()
    ax.plot(*zip(*gp_cost_per_iteration_Classical), label="Classical", color="midnightBlue")
    ax.plot(*zip(*gp_cost_per_iteration_UMAD), label="UMAD", color="mediumseagreen")
    ax.plot(*zip(*gp_cost_per_iteration_OneMutation), label="One Mutation", color="mediumpurple")
    ax.plot(*zip(*gp_cost_per_iteration_AlteredOneMutation), label="Altered One Mutation", color="orangered")
    ax.plot(*zip(*gp_cost_per_iteration_Interchanging), label="Interchanging", color="gold")
    ax.plot(*zip(*gp_cost_per_iteration_Scramble), label="Scramble", color="slategrey")
    ax.plot(*zip(*gp_cost_per_iteration_Reversing), label="Reversing", color="deepPink")
    ax.plot(*zip(*initial_error_line), label="Initial Error", color="black")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Error")
    ax.legend()
    ax.set_title("Error Progression in Example {}".format(example_name))

    plt.savefig("plots/error_progression_mutation.svg")
    fig.clf()
    plt.close


def plot_complexity_vs_solved_percentage():
    #fig, (ax2, ax3) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

    # Pixel
    domain = "pixel"
    gp_solved_percentage_Classical = gp_result_parser_pixel_Classical.solved_percentage_by_complexity(domain)
    gp_solved_percentage_UMAD = gp_result_parser_pixel_UMAD.solved_percentage_by_complexity(domain)
    gp_solved_percentage_OneMutation = gp_result_parser_pixel_OneMutation.solved_percentage_by_complexity(domain)
    gp_solved_percentage_AlteredOneMutation = gp_result_parser_pixel_AlteredOneMutation.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Interchanging = gp_result_parser_pixel_Interchanging.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Scramble = gp_result_parser_pixel_Scramble.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Reversing = gp_result_parser_pixel_Reversing.solved_percentage_by_complexity(domain)

    ax1.plot(gp_solved_percentage_Classical.keys(), gp_solved_percentage_Classical.values(), label="Classical", color="midnightBlue", marker="o")
    ax1.plot(gp_solved_percentage_UMAD.keys(), gp_solved_percentage_UMAD.values(), label="UMAD", color="mediumseagreen", marker="^")
    ax1.plot(gp_solved_percentage_OneMutation.keys(), gp_solved_percentage_OneMutation.values(), label="One Mutation", color="mediumpurple", marker="o")
    ax1.plot(gp_solved_percentage_AlteredOneMutation.keys(), gp_solved_percentage_AlteredOneMutation.values(), label="Altered One Mutation", color="orangered", marker="^")
    ax1.plot(gp_solved_percentage_Interchanging.keys(), gp_solved_percentage_Interchanging.values(), label="Interchanging", color="gold", marker="o")
    ax1.plot(gp_solved_percentage_Scramble.keys(), gp_solved_percentage_Scramble.values(), label="Scramble", color="slategrey", marker="^")
    ax1.plot(gp_solved_percentage_Reversing.keys(), gp_solved_percentage_Reversing.values(), label="Reversing", color="deepPink", marker="o")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Tasks Solved (%)")
    ax1.legend()
    ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_solved_percentage_Classical = gp_result_parser_robot_Classical.solved_percentage_by_complexity(domain)
    gp_solved_percentage_UMAD = gp_result_parser_robot_UMAD.solved_percentage_by_complexity(domain)
    gp_solved_percentage_OneMutation = gp_result_parser_robot_OneMutation.solved_percentage_by_complexity(domain)
    gp_solved_percentage_AlteredOneMutation = gp_result_parser_robot_AlteredOneMutation.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Interchanging = gp_result_parser_robot_Interchanging.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Scramble = gp_result_parser_robot_Scramble.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Reversing = gp_result_parser_robot_Reversing.solved_percentage_by_complexity(domain)

    ax2.plot(gp_solved_percentage_Classical.keys(), gp_solved_percentage_Classical.values(), label="Classical", color="midnightBlue", marker="o")
    ax2.plot(gp_solved_percentage_UMAD.keys(), gp_solved_percentage_UMAD.values(), label="UMAD", color="mediumseagreen", marker="^")
    ax2.plot(gp_solved_percentage_OneMutation.keys(), gp_solved_percentage_OneMutation.values(), label="One Mutation", color="mediumpurple", marker="o")
    ax2.plot(gp_solved_percentage_AlteredOneMutation.keys(), gp_solved_percentage_AlteredOneMutation.values(), label="Altered One Mutation", color="orangered", marker="^")
    ax2.plot(gp_solved_percentage_Interchanging.keys(), gp_solved_percentage_Interchanging.values(), label="Interchanging", color="gold", marker="o")
    ax2.plot(gp_solved_percentage_Scramble.keys(), gp_solved_percentage_Scramble.values(), label="Scramble", color="slategrey", marker="^")
    ax2.plot(gp_solved_percentage_Reversing.keys(), gp_solved_percentage_Reversing.values(), label="Reversing", color="deepPink", marker="o")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Tasks Solved (%)")
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_solved_percentage_Classical = gp_result_parser_string_Classical.solved_percentage_by_complexity(domain)
    gp_solved_percentage_UMAD = gp_result_parser_string_UMAD.solved_percentage_by_complexity(domain)
    gp_solved_percentage_OneMutation = gp_result_parser_string_OneMutation.solved_percentage_by_complexity(domain)
    gp_solved_percentage_AlteredOneMutation = gp_result_parser_string_AlteredOneMutation.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Interchanging = gp_result_parser_string_Interchanging.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Scramble = gp_result_parser_string_Scramble.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Reversing = gp_result_parser_string_Reversing.solved_percentage_by_complexity(domain)

    ax3.plot(gp_solved_percentage_Classical.keys(), gp_solved_percentage_Classical.values(), label="Classical", color="midnightBlue", marker="o")
    ax3.plot(gp_solved_percentage_UMAD.keys(), gp_solved_percentage_UMAD.values(), label="UMAD", color="mediumseagreen", marker="^")
    ax3.plot(gp_solved_percentage_OneMutation.keys(), gp_solved_percentage_OneMutation.values(), label="One Mutation", color="mediumpurple", marker="o")
    ax3.plot(gp_solved_percentage_AlteredOneMutation.keys(), gp_solved_percentage_AlteredOneMutation.values(), label="Altered One Mutation", color="orangered", marker="^")
    ax3.plot(gp_solved_percentage_Interchanging.keys(), gp_solved_percentage_Interchanging.values(), label="Interchanging", color="gold", marker="o")
    ax3.plot(gp_solved_percentage_Scramble.keys(), gp_solved_percentage_Scramble.values(), label="Scramble", color="slategrey", marker="^")
    ax3.plot(gp_solved_percentage_Reversing.keys(), gp_solved_percentage_Reversing.values(), label="Reversing", color="deepPink", marker="o")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Tasks Solved (%)")
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/solved_percentage_mutation.svg")
    fig.clf()
    plt.close


def plot_complexity_vs_avg_test_cost():
    fig, (ax2, ax3) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    # fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

    # Pixel
    domain = "pixel"
    gp_avg_test_cost_Classical = gp_result_parser_pixel_Classical.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_UMAD = gp_result_parser_pixel_UMAD.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_OneMutation = gp_result_parser_pixel_OneMutation.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_AlteredOneMutation = gp_result_parser_pixel_AlteredOneMutation.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Interchanging = gp_result_parser_pixel_Interchanging.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Scramble = gp_result_parser_pixel_Scramble.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Reversing = gp_result_parser_pixel_Reversing.avg_test_cost_by_complexity(domain)

    #ax1.plot(gp_avg_test_cost_Classical.keys(), gp_avg_test_cost_Classical.values(), label="Classical", color="midnightBlue", marker="o")
    #ax1.plot(gp_avg_test_cost_UMAD.keys(), gp_avg_test_cost_UMAD.values(), label="UMAD", color="mediumseagreen", marker="^")
    #ax1.plot(gp_avg_test_cost_OneMutation.keys(), gp_avg_test_cost_OneMutation.values(), label="OneMutation", color="orangered", marker="^")
    #ax1.plot(gp_avg_test_cost_AlteredOneMutation.keys(), gp_avg_test_cost_AlteredOneMutation.values(), label="Altered One Mutation", color="gold", marker="o")
    #ax1.plot(gp_avg_test_cost_Interchanging.keys(), gp_avg_test_cost_Interchanging.values(), label="Interchanging", color="slategrey", marker="^")
    #ax1.plot(gp_avg_test_cost_Scramble.keys(), gp_avg_test_cost_Scramble.values(), label="Scramble", color="deepPink", marker="o")
    #ax1.plot(gp_avg_test_cost_Reversing.keys(), gp_avg_test_cost_Reversing.values(), label="Reversing", color="peru", marker="^")
    #ax1.set_xlabel("Task Complexity")
    #ax1.set_ylabel("Average Test-Cost")
    #ax1.legend()
    #ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_avg_test_cost_Classical = gp_result_parser_robot_Classical.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_UMAD = gp_result_parser_robot_UMAD.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_OneMutation = gp_result_parser_robot_OneMutation.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_AlteredOneMutation = gp_result_parser_robot_AlteredOneMutation.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Interchanging = gp_result_parser_robot_Interchanging.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Scramble = gp_result_parser_robot_Scramble.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Reversing = gp_result_parser_robot_Reversing.avg_test_cost_by_complexity(domain)

    ax2.plot(gp_avg_test_cost_Classical.keys(), gp_avg_test_cost_Classical.values(), label="Classical", color="midnightBlue", marker="o")
    ax2.plot(gp_avg_test_cost_UMAD.keys(), gp_avg_test_cost_UMAD.values(), label="UMAD", color="mediumseagreen", marker="^")
    ax2.plot(gp_avg_test_cost_OneMutation.keys(), gp_avg_test_cost_OneMutation.values(), label="OneMutation", color="orangered", marker="^")
    ax2.plot(gp_avg_test_cost_AlteredOneMutation.keys(), gp_avg_test_cost_AlteredOneMutation.values(), label="Altered One Mutation", color="gold", marker="o")
    ax2.plot(gp_avg_test_cost_Interchanging.keys(), gp_avg_test_cost_Interchanging.values(), label="Interchanging", color="slategrey", marker="^")
    ax2.plot(gp_avg_test_cost_Scramble.keys(), gp_avg_test_cost_Scramble.values(), label="Scramble", color="deepPink", marker="o")
    ax2.plot(gp_avg_test_cost_Reversing.keys(), gp_avg_test_cost_Reversing.values(), label="Reversing", color="peru", marker="^")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Average Test-Cost")
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_avg_test_cost_Classical = gp_result_parser_string_Classical.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_UMAD = gp_result_parser_string_UMAD.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_OneMutation = gp_result_parser_string_OneMutation.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_AlteredOneMutation = gp_result_parser_string_AlteredOneMutation.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Interchanging = gp_result_parser_string_Interchanging.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Scramble = gp_result_parser_string_Scramble.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Reversing = gp_result_parser_string_Reversing.avg_test_cost_by_complexity(domain)

    ax3.plot(gp_avg_test_cost_Classical.keys(), gp_avg_test_cost_Classical.values(), label="Classical", color="midnightBlue", marker="o")
    ax3.plot(gp_avg_test_cost_UMAD.keys(), gp_avg_test_cost_UMAD.values(), label="UMAD", color="mediumseagreen", marker="^")
    ax3.plot(gp_avg_test_cost_OneMutation.keys(), gp_avg_test_cost_OneMutation.values(), label="OneMutation", color="orangered", marker="^")
    ax3.plot(gp_avg_test_cost_AlteredOneMutation.keys(), gp_avg_test_cost_AlteredOneMutation.values(), label="Altered One Mutation", color="gold", marker="o")
    ax3.plot(gp_avg_test_cost_Interchanging.keys(), gp_avg_test_cost_Interchanging.values(), label="Interchanging", color="slategrey", marker="^")
    ax3.plot(gp_avg_test_cost_Scramble.keys(), gp_avg_test_cost_Scramble.values(), label="Scramble", color="deepPink", marker="o")
    ax3.plot(gp_avg_test_cost_Reversing.keys(), gp_avg_test_cost_Reversing.values(), label="Reversing", color="peru", marker="^")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Average Test-Cost")
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/avg_test_cost_mutation.svg")
    fig.clf()
    plt.close

def plot_rel_improvement():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

    # Pixel
    domain = "pixel"
    gp_avg_rel_improvement_Classical = gp_result_parser_pixel_Classical.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_UMAD = gp_result_parser_pixel_UMAD.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_OneMutation = gp_result_parser_pixel_OneMutation.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_AlteredOneMutation = gp_result_parser_pixel_AlteredOneMutation.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Interchanging = gp_result_parser_pixel_Interchanging.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Scramble = gp_result_parser_pixel_Scramble.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Reversing = gp_result_parser_pixel_Reversing.rel_improvement_by_complexity(domain)

    ax1.plot(gp_avg_rel_improvement_Classical.keys(), gp_avg_rel_improvement_Classical.values(), label="Classical", color="midnightBlue",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_UMAD.keys(), gp_avg_rel_improvement_UMAD.values(), label="UMAD", color="mediumseagreen",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_OneMutation.keys(), gp_avg_rel_improvement_OneMutation.values(), label="One Mutation",
             color="mediumpurple",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_AlteredOneMutation.keys(), gp_avg_rel_improvement_AlteredOneMutation.values(), label="Altered One Mutation",
             color="orangered",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_Interchanging.keys(), gp_avg_rel_improvement_Interchanging.values(), label="Interchanging",
             color="gold",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_Scramble.keys(), gp_avg_rel_improvement_Scramble.values(), label="Scramble",
             color="slategrey",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_Reversing.keys(), gp_avg_rel_improvement_Reversing.values(), label="Reversing",
             color="deepPink",
             marker="o")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Avg. Relative Improvement (%)")
    ax1.set_ylim(ymin=0)
    ax1.legend()
    ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_avg_rel_improvement_Classical = gp_result_parser_robot_Classical.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_UMAD = gp_result_parser_robot_UMAD.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_OneMutation = gp_result_parser_robot_OneMutation.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_AlteredOneMutation = gp_result_parser_robot_AlteredOneMutation.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Interchanging = gp_result_parser_robot_Interchanging.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Scramble = gp_result_parser_robot_Scramble.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Reversing = gp_result_parser_robot_Reversing.rel_improvement_by_complexity(domain)

    ax2.plot(gp_avg_rel_improvement_Classical.keys(), gp_avg_rel_improvement_Classical.values(), label="Classical", color="midnightBlue",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_UMAD.keys(), gp_avg_rel_improvement_UMAD.values(), label="UMAD", color="mediumseagreen",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_OneMutation.keys(), gp_avg_rel_improvement_OneMutation.values(), label="One Mutation",
             color="mediumpurple",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_AlteredOneMutation.keys(), gp_avg_rel_improvement_AlteredOneMutation.values(), label="Altered One Mutation",
             color="orangered",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_Interchanging.keys(), gp_avg_rel_improvement_Interchanging.values(), label="Interchanging",
             color="gold",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_Scramble.keys(), gp_avg_rel_improvement_Scramble.values(), label="Scramble",
             color="slategrey",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_Reversing.keys(), gp_avg_rel_improvement_Reversing.values(), label="Reversing",
             color="deepPink",
             marker="o")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Avg. Relative Improvement (%)")
    ax2.set_ylim(ymin=0)
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_avg_rel_improvement_Classical = gp_result_parser_string_Classical.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_UMAD = gp_result_parser_string_UMAD.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_OneMutation = gp_result_parser_string_OneMutation.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_AlteredOneMutation = gp_result_parser_string_AlteredOneMutation.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Interchanging = gp_result_parser_string_Interchanging.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Scramble = gp_result_parser_string_Scramble.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Reversing = gp_result_parser_string_Reversing.rel_improvement_by_complexity(domain)

    ax3.plot(gp_avg_rel_improvement_Classical.keys(), gp_avg_rel_improvement_Classical.values(), label="Classical", color="midnightBlue",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_UMAD.keys(), gp_avg_rel_improvement_UMAD.values(), label="UMAD", color="mediumseagreen",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_OneMutation.keys(), gp_avg_rel_improvement_OneMutation.values(), label="One Mutation",
             color="mediumpurple",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_AlteredOneMutation.keys(), gp_avg_rel_improvement_AlteredOneMutation.values(), label="Altered One Mutation",
             color="orangered",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_Interchanging.keys(), gp_avg_rel_improvement_Interchanging.values(), label="Interchanging",
             color="gold",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_Scramble.keys(), gp_avg_rel_improvement_Scramble.values(), label="Scramble",
             color="slategrey",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_Reversing.keys(), gp_avg_rel_improvement_Reversing.values(), label="Reversing",
             color="deepPink",
             marker="o")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Avg. Relative Improvement (%)")
    ax3.set_ylim(ymin=0)
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/relative_improvement_mutation.svg")
    fig.clf()
    plt.close


plot_rel_improvement()
plot_complexity_vs_solved_percentage()
plot_error_progression("string", "strings/1-58-1.pl")
plot_complexity_vs_avg_test_cost()
