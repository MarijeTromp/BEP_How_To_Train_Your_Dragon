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
# SUSOriginal
gp_path_to_file_pixel_SUSOriginal = "../../../../results/pixel/SUSOriginal.txt"
gp_path_to_file_robot_SUSOriginal = "../../../../results/robot/SUSOriginal.txt"
gp_path_to_file_string_SUSOriginal = "../../../../results/string/SUSOriginal.txt"

gp_result_parser_pixel_SUSOriginal = ResultParser(gp_path_to_file_pixel_SUSOriginal)
gp_result_parser_robot_SUSOriginal = ResultParser(gp_path_to_file_robot_SUSOriginal)
gp_result_parser_string_SUSOriginal = ResultParser(gp_path_to_file_string_SUSOriginal)

# SUS
gp_path_to_file_pixel_SUS = "../../../../results/pixel/SUS.txt"
gp_path_to_file_robot_SUS = "../../../../results/robot/SUS.txt"
gp_path_to_file_string_SUS = "../../../../results/string/SUS.txt"

gp_result_parser_pixel_SUS = ResultParser(gp_path_to_file_pixel_SUS)
gp_result_parser_robot_SUS = ResultParser(gp_path_to_file_robot_SUS)
gp_result_parser_string_SUS = ResultParser(gp_path_to_file_string_SUS)

# RWS
gp_path_to_file_pixel_RWS = "../../../../results/pixel/RWS.txt"
gp_path_to_file_robot_RWS = "../../../../results/robot/RWS.txt"
gp_path_to_file_string_RWS = "../../../../results/string/RWS.txt"

gp_result_parser_pixel_RWS = ResultParser(gp_path_to_file_pixel_RWS)
gp_result_parser_robot_RWS = ResultParser(gp_path_to_file_robot_RWS)
gp_result_parser_string_RWS = ResultParser(gp_path_to_file_string_RWS)

# Lexicase
gp_path_to_file_pixel_Lexicase = "../../../../results/pixel/Lexicase.txt"
gp_path_to_file_robot_Lexicase = "../../../../results/robot/Lexicase.txt"
gp_path_to_file_string_Lexicase = "../../../../results/string/Lexicase.txt"

gp_result_parser_pixel_Lexicase = ResultParser(gp_path_to_file_pixel_Lexicase)
gp_result_parser_robot_Lexicase = ResultParser(gp_path_to_file_robot_Lexicase)
gp_result_parser_string_Lexicase = ResultParser(gp_path_to_file_string_Lexicase)

# DownsampledLexicase
gp_path_to_file_pixel_DownsampledLexicase = "../../../../results/pixel/DownsampledLexicase.txt"
gp_path_to_file_robot_DownsampledLexicase = "../../../../results/robot/DownsampledLexicase.txt"
gp_path_to_file_string_DownsampledLexicase = "../../../../results/string/DownsampledLexicase.txt"

gp_result_parser_pixel_DownsampledLexicase = ResultParser(gp_path_to_file_pixel_DownsampledLexicase)
gp_result_parser_robot_DownsampledLexicase = ResultParser(gp_path_to_file_robot_DownsampledLexicase)
gp_result_parser_string_DownsampledLexicase = ResultParser(gp_path_to_file_string_DownsampledLexicase)

# CombinedLexicase
gp_path_to_file_pixel_CombinedLexicase = "../../../../results/pixel/CombinedLexicase.txt"
gp_path_to_file_robot_CombinedLexicase = "../../../../results/robot/CombinedLexicase.txt"
gp_path_to_file_string_CombinedLexicase = "../../../../results/string/CombinedLexicase.txt"

gp_result_parser_pixel_CombinedLexicase = ResultParser(gp_path_to_file_pixel_CombinedLexicase)
gp_result_parser_robot_CombinedLexicase = ResultParser(gp_path_to_file_robot_CombinedLexicase)
gp_result_parser_string_CombinedLexicase = ResultParser(gp_path_to_file_string_CombinedLexicase)

# Tournament
gp_path_to_file_pixel_Tournament = "../../../../results/pixel/Tournament.txt"
gp_path_to_file_robot_Tournament = "../../../../results/robot/Tournament.txt"
gp_path_to_file_string_Tournament = "../../../../results/string/Tournament.txt"

gp_result_parser_pixel_Tournament = ResultParser(gp_path_to_file_pixel_Tournament)
gp_result_parser_robot_Tournament = ResultParser(gp_path_to_file_robot_Tournament)
gp_result_parser_string_Tournament = ResultParser(gp_path_to_file_string_Tournament)

# Truncation
gp_path_to_file_pixel_Truncation = "../../../../results/pixel/Truncation.txt"
gp_path_to_file_robot_Truncation = "../../../../results/robot/Truncation.txt"
gp_path_to_file_string_Truncation = "../../../../results/string/Truncation.txt"

gp_result_parser_pixel_Truncation = ResultParser(gp_path_to_file_pixel_Truncation)
gp_result_parser_robot_Truncation = ResultParser(gp_path_to_file_robot_Truncation)
gp_result_parser_string_Truncation = ResultParser(gp_path_to_file_string_Truncation)


def plot_error_progression(domain, example_name):
    initial_error = 0.0

    gp_cost_per_iteration_SUS = []
    if (domain == "pixel"):
        initial_error = gp_result_parser_pixel_SUS.get_initial_error(example_name)
        gp_cost_per_iteration_SUS = gp_result_parser_pixel_SUS.error_progression(example_name)
    elif (domain == "robot"):
        initial_error = gp_result_parser_robot_SUS.get_initial_error(example_name)
        gp_cost_per_iteration_SUS = gp_result_parser_robot_SUS.error_progression(example_name)
    elif (domain == "string"):
        initial_error = gp_result_parser_string_SUS.get_initial_error(example_name)
        gp_cost_per_iteration_SUS = gp_result_parser_string_SUS.error_progression(example_name)

    initial_error_line = [(i, initial_error) for i in [*range(0, len(gp_cost_per_iteration_SUS))]]

    gp_cost_per_iteration_SUSOriginal = []
    if (domain == "pixel"):
        gp_cost_per_iteration_SUSOriginal = gp_result_parser_pixel_SUSOriginal.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_SUSOriginal = gp_result_parser_robot_SUSOriginal.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_SUSOriginal = gp_result_parser_string_SUSOriginal.error_progression(example_name)

    gp_cost_per_iteration_RWS = []
    if (domain == "pixel"):
        gp_cost_per_iteration_RWS = gp_result_parser_pixel_RWS.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_RWS = gp_result_parser_robot_RWS.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_RWS= gp_result_parser_string_RWS.error_progression(example_name)

    gp_cost_per_iteration_Lexicase = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Lexicase = gp_result_parser_pixel_Lexicase.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Lexicase = gp_result_parser_robot_Lexicase.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Lexicase = gp_result_parser_string_Lexicase.error_progression(example_name)

    gp_cost_per_iteration_DownsampledLexicase = []
    if (domain == "pixel"):
        gp_cost_per_iteration_DownsampledLexicase = gp_result_parser_pixel_DownsampledLexicase.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_DownsampledLexicase = gp_result_parser_robot_DownsampledLexicase.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_DownsampledLexicase = gp_result_parser_string_DownsampledLexicase.error_progression(example_name)

    gp_cost_per_iteration_CombinedLexicase = []
    if (domain == "pixel"):
        gp_cost_per_iteration_CombinedLexicase = gp_result_parser_pixel_CombinedLexicase.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_CombinedLexicase = gp_result_parser_robot_CombinedLexicase.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_CombinedLexicase = gp_result_parser_string_CombinedLexicase.error_progression(example_name)

    gp_cost_per_iteration_Tournament = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Tournament = gp_result_parser_pixel_Tournament.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Tournament = gp_result_parser_robot_Tournament.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Tournament = gp_result_parser_string_Tournament.error_progression(example_name)

    gp_cost_per_iteration_Truncation = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Truncation = gp_result_parser_pixel_Truncation.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Truncation = gp_result_parser_robot_Truncation.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Truncation = gp_result_parser_string_Truncation.error_progression(example_name)

    fig, ax = plt.subplots()
    ax.plot(*zip(*gp_cost_per_iteration_SUSOriginal), label="Original SUS", color="midnightBlue")
    ax.plot(*zip(*gp_cost_per_iteration_SUS), label="SUS", color="mediumseagreen")
    ax.plot(*zip(*gp_cost_per_iteration_RWS), label="RWS", color="mediumpurple")
    ax.plot(*zip(*gp_cost_per_iteration_Lexicase), label="Lexicase", color="orangered")
    ax.plot(*zip(*gp_cost_per_iteration_DownsampledLexicase), label="Downsampled Lexicase", color="gold")
    ax.plot(*zip(*gp_cost_per_iteration_CombinedLexicase), label="Combined Lexicase", color="slategrey")
    ax.plot(*zip(*gp_cost_per_iteration_Tournament), label="Tournament", color="deepPink")
    ax.plot(*zip(*gp_cost_per_iteration_Truncation), label="Truncation", color="peru")
    ax.plot(*zip(*initial_error_line), label="Initial Error", color="black")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Error")
    ax.legend()
    ax.set_title("Error Progression in Example {}".format(example_name))

    plt.savefig("plots/error_progression_selection.svg")
    fig.clf()
    plt.close


def plot_complexity_vs_solved_percentage():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

    # Pixel
    domain = "pixel"
    gp_solved_percentage_SUSOriginal = gp_result_parser_pixel_SUSOriginal.solved_percentage_by_complexity(domain)
    gp_solved_percentage_SUS = gp_result_parser_pixel_SUS.solved_percentage_by_complexity(domain)
    gp_solved_percentage_RWS = gp_result_parser_pixel_RWS.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Lexicase = gp_result_parser_pixel_Lexicase.solved_percentage_by_complexity(domain)
    gp_solved_percentage_DownsampledLexicase = gp_result_parser_pixel_DownsampledLexicase.solved_percentage_by_complexity(domain)
    gp_solved_percentage_CombinedLexicase = gp_result_parser_pixel_CombinedLexicase.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Tournament = gp_result_parser_pixel_Tournament.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Truncation = gp_result_parser_pixel_Truncation.solved_percentage_by_complexity(domain)

    ax1.plot(gp_solved_percentage_SUSOriginal.keys(), gp_solved_percentage_SUSOriginal.values(), label="Original SUS", color="midnightBlue", marker="o")
    ax1.plot(gp_solved_percentage_SUS.keys(), gp_solved_percentage_SUS.values(), label="SUS", color="mediumseagreen", marker="^")
    ax1.plot(gp_solved_percentage_RWS.keys(), gp_solved_percentage_RWS.values(), label="RWS", color="mediumpurple", marker="o")
    ax1.plot(gp_solved_percentage_Lexicase.keys(), gp_solved_percentage_Lexicase.values(), label="Lexicase", color="orangered", marker="^")
    ax1.plot(gp_solved_percentage_DownsampledLexicase.keys(), gp_solved_percentage_DownsampledLexicase.values(), label="Downsampled Lexicase", color="gold", marker="o")
    ax1.plot(gp_solved_percentage_CombinedLexicase.keys(), gp_solved_percentage_CombinedLexicase.values(), label="Combined Lexicase", color="slategrey", marker="^")
    ax1.plot(gp_solved_percentage_Tournament.keys(), gp_solved_percentage_Tournament.values(), label="Tournament", color="deepPink", marker="o")
    ax1.plot(gp_solved_percentage_Truncation.keys(), gp_solved_percentage_Truncation.values(), label="Truncation", color="peru", marker="^")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Tasks Solved (%)")
    ax1.legend()
    ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_solved_percentage_SUSOriginal = gp_result_parser_robot_SUSOriginal.solved_percentage_by_complexity(domain)
    gp_solved_percentage_SUS = gp_result_parser_robot_SUS.solved_percentage_by_complexity(domain)
    gp_solved_percentage_RWS = gp_result_parser_robot_RWS.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Lexicase = gp_result_parser_robot_Lexicase.solved_percentage_by_complexity(domain)
    gp_solved_percentage_DownsampledLexicase = gp_result_parser_robot_DownsampledLexicase.solved_percentage_by_complexity(domain)
    gp_solved_percentage_CombinedLexicase = gp_result_parser_robot_CombinedLexicase.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Tournament = gp_result_parser_robot_Tournament.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Truncation = gp_result_parser_robot_Truncation.solved_percentage_by_complexity(domain)

    ax2.plot(gp_solved_percentage_SUSOriginal.keys(), gp_solved_percentage_SUSOriginal.values(), label="Original SUS", color="midnightBlue", marker="o")
    ax2.plot(gp_solved_percentage_SUS.keys(), gp_solved_percentage_SUS.values(), label="SUS", color="mediumseagreen", marker="^")
    ax2.plot(gp_solved_percentage_RWS.keys(), gp_solved_percentage_RWS.values(), label="RWS", color="mediumpurple", marker="o")
    ax2.plot(gp_solved_percentage_Lexicase.keys(), gp_solved_percentage_Lexicase.values(), label="Lexicase", color="orangered", marker="^")
    ax2.plot(gp_solved_percentage_DownsampledLexicase.keys(), gp_solved_percentage_DownsampledLexicase.values(), label="Downsampled Lexicase", color="gold", marker="o")
    ax2.plot(gp_solved_percentage_CombinedLexicase.keys(), gp_solved_percentage_CombinedLexicase.values(), label="Combined Lexicase", color="slategrey", marker="^")
    ax2.plot(gp_solved_percentage_Tournament.keys(), gp_solved_percentage_Tournament.values(), label="Tournament", color="deepPink", marker="o")
    ax2.plot(gp_solved_percentage_Truncation.keys(), gp_solved_percentage_Truncation.values(), label="Truncation", color="peru", marker="^")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Tasks Solved (%)")
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_solved_percentage_SUSOriginal = gp_result_parser_string_SUSOriginal.solved_percentage_by_complexity(domain)
    gp_solved_percentage_SUS = gp_result_parser_string_SUS.solved_percentage_by_complexity(domain)
    gp_solved_percentage_RWS = gp_result_parser_string_RWS.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Lexicase = gp_result_parser_string_Lexicase.solved_percentage_by_complexity(domain)
    gp_solved_percentage_DownsampledLexicase = gp_result_parser_string_DownsampledLexicase.solved_percentage_by_complexity(domain)
    gp_solved_percentage_CombinedLexicase = gp_result_parser_string_CombinedLexicase.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Tournament = gp_result_parser_string_Tournament.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Truncation = gp_result_parser_string_Truncation.solved_percentage_by_complexity(domain)

    ax3.plot(gp_solved_percentage_SUSOriginal.keys(), gp_solved_percentage_SUSOriginal.values(), label="Original SUS", color="midnightBlue", marker="o")
    ax3.plot(gp_solved_percentage_SUS.keys(), gp_solved_percentage_SUS.values(), label="SUS", color="mediumseagreen", marker="^")
    ax3.plot(gp_solved_percentage_RWS.keys(), gp_solved_percentage_RWS.values(), label="RWS", color="mediumpurple", marker="o")
    ax3.plot(gp_solved_percentage_Lexicase.keys(), gp_solved_percentage_Lexicase.values(), label="Lexicase", color="orangered", marker="^")
    ax3.plot(gp_solved_percentage_DownsampledLexicase.keys(), gp_solved_percentage_DownsampledLexicase.values(), label="Downsampled Lexicase", color="gold", marker="o")
    ax3.plot(gp_solved_percentage_CombinedLexicase.keys(), gp_solved_percentage_CombinedLexicase.values(), label="Combined Lexicase", color="slategrey", marker="^")
    ax3.plot(gp_solved_percentage_Tournament.keys(), gp_solved_percentage_Tournament.values(), label="Tournament", color="deepPink", marker="o")
    ax3.plot(gp_solved_percentage_Truncation.keys(), gp_solved_percentage_Truncation.values(), label="Truncation", color="peru", marker="^")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Tasks Solved (%)")
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/solved_percentage_selection.svg")
    fig.clf()
    plt.close


def plot_complexity_vs_avg_test_cost():
    fig, (ax2, ax3) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

    # Pixel
    domain = "pixel"
    gp_avg_test_cost_SUSOriginal = gp_result_parser_pixel_SUSOriginal.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_SUS = gp_result_parser_pixel_SUS.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_RWS = gp_result_parser_pixel_RWS.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Lexicase = gp_result_parser_pixel_Lexicase.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_DownsampledLexicase = gp_result_parser_pixel_DownsampledLexicase.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_CombinedLexicase = gp_result_parser_pixel_CombinedLexicase.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Tournament = gp_result_parser_pixel_Tournament.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Truncation = gp_result_parser_pixel_Truncation.avg_test_cost_by_complexity(domain)

    #ax1.plot(gp_avg_test_cost_SUSOriginal.keys(), gp_avg_test_cost_SUSOriginal.values(), label="Original SUS", color="midnightBlue", marker="o")
    #ax1.plot(gp_avg_test_cost_SUS.keys(), gp_avg_test_cost_SUS.values(), label="SUS", color="mediumseagreen", marker="^")
    #ax1.plot(gp_avg_test_cost_RWS.keys(), gp_avg_test_cost_RWS.values(), label="RWS", color="mediumpurple", marker="o")
    #ax1.plot(gp_avg_test_cost_Lexicase.keys(), gp_avg_test_cost_Lexicase.values(), label="Lexicase", color="orangered", marker="^")
    #ax1.plot(gp_avg_test_cost_DownsampledLexicase.keys(), gp_avg_test_cost_DownsampledLexicase.values(), label="Downsampled Lexicase", color="gold", marker="o")
    #ax1.plot(gp_avg_test_cost_CombinedLexicase.keys(), gp_avg_test_cost_CombinedLexicase.values(), label="Combined Lexicase", color="slategrey", marker="^")
    #ax1.plot(gp_avg_test_cost_Tournament.keys(), gp_avg_test_cost_Tournament.values(), label="Tournament", color="deepPink", marker="o")
    #ax1.plot(gp_avg_test_cost_Truncation.keys(), gp_avg_test_cost_Truncation.values(), label="Truncation", color="peru", marker="^")
    #ax1.set_xlabel("Task Complexity")
    #ax1.set_ylabel("Average Test-Cost")
    #ax1.legend()
    #ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_avg_test_cost_SUSOriginal = gp_result_parser_robot_SUSOriginal.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_SUS = gp_result_parser_robot_SUS.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_RWS = gp_result_parser_robot_RWS.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Lexicase = gp_result_parser_robot_Lexicase.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_DownsampledLexicase = gp_result_parser_robot_DownsampledLexicase.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_CombinedLexicase = gp_result_parser_robot_CombinedLexicase.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Tournament = gp_result_parser_robot_Tournament.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Truncation = gp_result_parser_robot_Truncation.avg_test_cost_by_complexity(domain)

    ax2.plot(gp_avg_test_cost_SUSOriginal.keys(), gp_avg_test_cost_SUSOriginal.values(), label="Original SUS", color="midnightBlue", marker="o")
    ax2.plot(gp_avg_test_cost_SUS.keys(), gp_avg_test_cost_SUS.values(), label="SUS", color="mediumseagreen", marker="^")
    ax2.plot(gp_avg_test_cost_RWS.keys(), gp_avg_test_cost_RWS.values(), label="RWS", color="mediumpurple", marker="o")
    ax2.plot(gp_avg_test_cost_Lexicase.keys(), gp_avg_test_cost_Lexicase.values(), label="Lexicase", color="orangered", marker="^")
    ax2.plot(gp_avg_test_cost_DownsampledLexicase.keys(), gp_avg_test_cost_DownsampledLexicase.values(), label="Downsampled Lexicase", color="gold", marker="o")
    ax2.plot(gp_avg_test_cost_CombinedLexicase.keys(), gp_avg_test_cost_CombinedLexicase.values(), label="Combined Lexicase", color="slategrey", marker="^")
    ax2.plot(gp_avg_test_cost_Tournament.keys(), gp_avg_test_cost_Tournament.values(), label="Tournament", color="deepPink", marker="o")
    ax2.plot(gp_avg_test_cost_Truncation.keys(), gp_avg_test_cost_Truncation.values(), label="Truncation", color="peru", marker="^")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Average Test-Cost")
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_avg_test_cost_SUSOriginal = gp_result_parser_string_SUSOriginal.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_SUS = gp_result_parser_string_SUS.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_RWS = gp_result_parser_string_RWS.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Lexicase = gp_result_parser_string_Lexicase.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_DownsampledLexicase = gp_result_parser_string_DownsampledLexicase.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_CombinedLexicase = gp_result_parser_string_CombinedLexicase.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Tournament = gp_result_parser_string_Tournament.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Truncation = gp_result_parser_string_Truncation.avg_test_cost_by_complexity(domain)

    ax3.plot(gp_avg_test_cost_SUSOriginal.keys(), gp_avg_test_cost_SUSOriginal.values(), label="Original SUS", color="midnightBlue", marker="o")
    ax3.plot(gp_avg_test_cost_SUS.keys(), gp_avg_test_cost_SUS.values(), label="SUS", color="mediumseagreen", marker="^")
    ax3.plot(gp_avg_test_cost_RWS.keys(), gp_avg_test_cost_RWS.values(), label="RWS", color="mediumpurple", marker="o")
    ax3.plot(gp_avg_test_cost_Lexicase.keys(), gp_avg_test_cost_Lexicase.values(), label="Lexicase", color="orangered", marker="^")
    ax3.plot(gp_avg_test_cost_DownsampledLexicase.keys(), gp_avg_test_cost_DownsampledLexicase.values(), label="Downsampled Lexicase", color="gold", marker="o")
    ax3.plot(gp_avg_test_cost_CombinedLexicase.keys(), gp_avg_test_cost_CombinedLexicase.values(), label="Combined Lexicase", color="slategrey", marker="^")
    ax3.plot(gp_avg_test_cost_Tournament.keys(), gp_avg_test_cost_Tournament.values(), label="Tournament", color="deepPink", marker="o")
    ax3.plot(gp_avg_test_cost_Truncation.keys(), gp_avg_test_cost_Truncation.values(), label="Truncation", color="peru", marker="^")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Average Test-Cost")
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/avg_test_cost_selection.svg")
    fig.clf()
    plt.close

def plot_rel_improvement():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

    # Pixel
    domain = "pixel"
    gp_avg_rel_improvement_SUSOriginal = gp_result_parser_pixel_SUSOriginal.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_SUS = gp_result_parser_pixel_SUS.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_RWS = gp_result_parser_pixel_RWS.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Lexicase = gp_result_parser_pixel_Lexicase.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_DownsampledLexicase = gp_result_parser_pixel_DownsampledLexicase.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_CombinedLexicase = gp_result_parser_pixel_CombinedLexicase.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Tournament = gp_result_parser_pixel_Tournament.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Truncation = gp_result_parser_pixel_Truncation.rel_improvement_by_complexity(domain)

    ax1.plot(gp_avg_rel_improvement_SUSOriginal.keys(), gp_avg_rel_improvement_SUSOriginal.values(), label="Original SUS", color="midnightBlue",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_SUS.keys(), gp_avg_rel_improvement_SUS.values(), label="SUS", color="mediumseagreen",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_RWS.keys(), gp_avg_rel_improvement_RWS.values(), label="RWS",
             color="mediumpurple",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_Lexicase.keys(), gp_avg_rel_improvement_Lexicase.values(), label="Lexicase",
             color="orangered",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_DownsampledLexicase.keys(), gp_avg_rel_improvement_DownsampledLexicase.values(), label="Downsampled Lexicase",
             color="gold",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_CombinedLexicase.keys(), gp_avg_rel_improvement_CombinedLexicase.values(), label="Combined Lexicase",
             color="slategrey",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_Tournament.keys(), gp_avg_rel_improvement_Tournament.values(), label="Tournament",
             color="deepPink",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_Truncation.keys(), gp_avg_rel_improvement_Truncation.values(), label="Truncation",
             color="peru",
             marker="^")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Avg. Relative Improvement (%)")
    ax1.set_ylim(ymin=0)
    ax1.legend()
    ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_avg_rel_improvement_SUSOriginal = gp_result_parser_robot_SUSOriginal.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_SUS = gp_result_parser_robot_SUS.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_RWS = gp_result_parser_robot_RWS.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Lexicase = gp_result_parser_robot_Lexicase.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_DownsampledLexicase = gp_result_parser_robot_DownsampledLexicase.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_CombinedLexicase = gp_result_parser_robot_CombinedLexicase.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Tournament = gp_result_parser_robot_Tournament.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Truncation = gp_result_parser_robot_Truncation.rel_improvement_by_complexity(domain)

    ax2.plot(gp_avg_rel_improvement_SUSOriginal.keys(), gp_avg_rel_improvement_SUSOriginal.values(), label="Original SUS", color="midnightBlue",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_SUS.keys(), gp_avg_rel_improvement_SUS.values(), label="SUS", color="mediumseagreen",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_RWS.keys(), gp_avg_rel_improvement_RWS.values(), label="RWS",
             color="mediumpurple",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_Lexicase.keys(), gp_avg_rel_improvement_Lexicase.values(), label="Lexicase",
             color="orangered",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_DownsampledLexicase.keys(), gp_avg_rel_improvement_DownsampledLexicase.values(), label="Downsampled Lexicase",
             color="gold",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_CombinedLexicase.keys(), gp_avg_rel_improvement_CombinedLexicase.values(), label="Combined Lexicase",
             color="slategrey",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_Tournament.keys(), gp_avg_rel_improvement_Tournament.values(), label="Tournament",
             color="deepPink",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_Truncation.keys(), gp_avg_rel_improvement_Truncation.values(), label="Truncation",
             color="peru",
             marker="^")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Avg. Relative Improvement (%)")
    ax2.set_ylim(ymin=0)
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_avg_rel_improvement_SUSOriginal = gp_result_parser_string_SUSOriginal.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_SUS = gp_result_parser_string_SUS.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_RWS = gp_result_parser_string_RWS.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Lexicase = gp_result_parser_string_Lexicase.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_DownsampledLexicase = gp_result_parser_string_DownsampledLexicase.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_CombinedLexicase = gp_result_parser_string_CombinedLexicase.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Tournament = gp_result_parser_string_Tournament.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Truncation = gp_result_parser_string_Truncation.rel_improvement_by_complexity(domain)

    ax3.plot(gp_avg_rel_improvement_SUSOriginal.keys(), gp_avg_rel_improvement_SUSOriginal.values(), label="Original SUS", color="midnightBlue",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_SUS.keys(), gp_avg_rel_improvement_SUS.values(), label="SUS", color="mediumseagreen",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_RWS.keys(), gp_avg_rel_improvement_RWS.values(), label="RWS",
             color="mediumpurple",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_Lexicase.keys(), gp_avg_rel_improvement_Lexicase.values(), label="Lexicase",
             color="orangered",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_DownsampledLexicase.keys(), gp_avg_rel_improvement_DownsampledLexicase.values(), label="Downsampled Lexicase",
             color="gold",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_CombinedLexicase.keys(), gp_avg_rel_improvement_CombinedLexicase.values(), label="Combined Lexicase",
             color="slategrey",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_Tournament.keys(), gp_avg_rel_improvement_Tournament.values(), label="Tournament",
             color="deepPink",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_Truncation.keys(), gp_avg_rel_improvement_Truncation.values(), label="Truncation",
             color="peru",
             marker="^")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Avg. Relative Improvement (%)")
    ax3.set_ylim(ymin=0)
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/relative_improvement_selection.svg")
    fig.clf()
    plt.close


plot_rel_improvement()
plot_complexity_vs_solved_percentage()
plot_error_progression("string", "strings/1-58-1.pl")
plot_complexity_vs_avg_test_cost()
