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
# Brute
gp_path_to_file_pixel_Brute = "../../../../results/pixel/Brute.txt"
gp_path_to_file_robot_Brute = "../../../../results/robot/Brute.txt"
gp_path_to_file_string_Brute = "../../../../results/string/Brute.txt"

gp_result_parser_pixel_Brute = ResultParser(gp_path_to_file_pixel_Brute)
gp_result_parser_robot_Brute = ResultParser(gp_path_to_file_robot_Brute)
gp_result_parser_string_Brute = ResultParser(gp_path_to_file_string_Brute)

# VanillaGP
gp_path_to_file_pixel_VanillaGP = "../../../../results/pixel/VanillaGP.txt"
gp_path_to_file_robot_VanillaGP = "../../../../results/robot/VanillaGP.txt"
gp_path_to_file_string_VanillaGP = "../../../../results/string/VanillaGP.txt"

gp_result_parser_pixel_VanillaGP = ResultParser(gp_path_to_file_pixel_VanillaGP)
gp_result_parser_robot_VanillaGP = ResultParser(gp_path_to_file_robot_VanillaGP)
gp_result_parser_string_VanillaGP = ResultParser(gp_path_to_file_string_VanillaGP)

# Combination1
gp_path_to_file_pixel_Combination1 = "../../../../results/pixel/Combination1.txt"
gp_path_to_file_robot_Combination1 = "../../../../results/robot/Combination1.txt"
gp_path_to_file_string_Combination1 = "../../../../results/string/Combination1.txt"

gp_result_parser_pixel_Combination1 = ResultParser(gp_path_to_file_pixel_Combination1)
gp_result_parser_robot_Combination1 = ResultParser(gp_path_to_file_robot_Combination1)
gp_result_parser_string_Combination1 = ResultParser(gp_path_to_file_string_Combination1)

# Combination2
gp_path_to_file_pixel_Combination2 = "../../../../results/pixel/Combination2.txt"
gp_path_to_file_robot_Combination2 = "../../../../results/robot/Combination2.txt"
gp_path_to_file_string_Combination2 = "../../../../results/string/Combination2.txt"

gp_result_parser_pixel_Combination2 = ResultParser(gp_path_to_file_pixel_Combination2)
gp_result_parser_robot_Combination2 = ResultParser(gp_path_to_file_robot_Combination2)
gp_result_parser_string_Combination2 = ResultParser(gp_path_to_file_string_Combination2)

# Combination3
gp_path_to_file_pixel_Combination3 = "../../../../results/pixel/Combination3.txt"
gp_path_to_file_robot_Combination3 = "../../../../results/robot/Combination3.txt"
gp_path_to_file_string_Combination3 = "../../../../results/string/Combination3.txt"

gp_result_parser_pixel_Combination3 = ResultParser(gp_path_to_file_pixel_Combination3)
gp_result_parser_robot_Combination3 = ResultParser(gp_path_to_file_robot_Combination3)
gp_result_parser_string_Combination3 = ResultParser(gp_path_to_file_string_Combination3)

# Combination4
gp_path_to_file_pixel_Combination4 = "../../../../results/pixel/Combination4.txt"
gp_path_to_file_robot_Combination4 = "../../../../results/robot/Combination4.txt"
gp_path_to_file_string_Combination4 = "../../../../results/string/Combination4.txt"

gp_result_parser_pixel_Combination4 = ResultParser(gp_path_to_file_pixel_Combination4)
gp_result_parser_robot_Combination4 = ResultParser(gp_path_to_file_robot_Combination4)
gp_result_parser_string_Combination4 = ResultParser(gp_path_to_file_string_Combination4)

# Combination5
gp_path_to_file_pixel_Combination5 = "../../../../results/pixel/Combination5.txt"
gp_path_to_file_robot_Combination5 = "../../../../results/robot/Combination5.txt"
gp_path_to_file_string_Combination5 = "../../../../results/string/Combination5.txt"

gp_result_parser_pixel_Combination5 = ResultParser(gp_path_to_file_pixel_Combination5)
gp_result_parser_robot_Combination5 = ResultParser(gp_path_to_file_robot_Combination5)
gp_result_parser_string_Combination5 = ResultParser(gp_path_to_file_string_Combination5)

# Combination6
gp_path_to_file_pixel_Combination6 = "../../../../results/pixel/Combination6.txt"
gp_path_to_file_robot_Combination6 = "../../../../results/robot/Combination6.txt"
gp_path_to_file_string_Combination6 = "../../../../results/string/Combination6.txt"

gp_result_parser_pixel_Combination6 = ResultParser(gp_path_to_file_pixel_Combination6)
gp_result_parser_robot_Combination6 = ResultParser(gp_path_to_file_robot_Combination6)
gp_result_parser_string_Combination6 = ResultParser(gp_path_to_file_string_Combination6)

# Combination7
gp_path_to_file_pixel_Combination7 = "../../../../results/pixel/Combination7.txt"
gp_path_to_file_robot_Combination7 = "../../../../results/robot/Combination7.txt"
gp_path_to_file_string_Combination7 = "../../../../results/string/Combination7.txt"

gp_result_parser_pixel_Combination7 = ResultParser(gp_path_to_file_pixel_Combination7)
gp_result_parser_robot_Combination7 = ResultParser(gp_path_to_file_robot_Combination7)
gp_result_parser_string_Combination7 = ResultParser(gp_path_to_file_string_Combination7)

# Combination8
gp_path_to_file_pixel_Combination8 = "../../../../results/pixel/Combination8.txt"
gp_path_to_file_robot_Combination8 = "../../../../results/robot/Combination8.txt"
gp_path_to_file_string_Combination8 = "../../../../results/string/Combination8.txt"

gp_result_parser_pixel_Combination8 = ResultParser(gp_path_to_file_pixel_Combination8)
gp_result_parser_robot_Combination8 = ResultParser(gp_path_to_file_robot_Combination8)
gp_result_parser_string_Combination8 = ResultParser(gp_path_to_file_string_Combination8)

# Combination9
gp_path_to_file_pixel_Combination9 = "../../../../results/pixel/Combination9.txt"
gp_path_to_file_robot_Combination9 = "../../../../results/robot/Combination9.txt"
gp_path_to_file_string_Combination9 = "../../../../results/string/Combination9.txt"

gp_result_parser_pixel_Combination9 = ResultParser(gp_path_to_file_pixel_Combination9)
gp_result_parser_robot_Combination9 = ResultParser(gp_path_to_file_robot_Combination9)
gp_result_parser_string_Combination9 = ResultParser(gp_path_to_file_string_Combination9)

# Combination10
gp_path_to_file_pixel_Combination10 = "../../../../results/pixel/Combination10.txt"
gp_path_to_file_robot_Combination10 = "../../../../results/robot/Combination10.txt"
gp_path_to_file_string_Combination10 = "../../../../results/string/Combination10.txt"

gp_result_parser_pixel_Combination10 = ResultParser(gp_path_to_file_pixel_Combination10)
gp_result_parser_robot_Combination10 = ResultParser(gp_path_to_file_robot_Combination10)
gp_result_parser_string_Combination10 = ResultParser(gp_path_to_file_string_Combination10)

# Combination11
gp_path_to_file_pixel_Combination11 = "../../../../results/pixel/Combination11.txt"
gp_path_to_file_robot_Combination11 = "../../../../results/robot/Combination11.txt"
gp_path_to_file_string_Combination11 = "../../../../results/string/Combination11.txt"

gp_result_parser_pixel_Combination11 = ResultParser(gp_path_to_file_pixel_Combination11)
gp_result_parser_robot_Combination11 = ResultParser(gp_path_to_file_robot_Combination11)
gp_result_parser_string_Combination11 = ResultParser(gp_path_to_file_string_Combination11)

# Combination12
gp_path_to_file_pixel_Combination12 = "../../../../results/pixel/Combination12.txt"
gp_path_to_file_robot_Combination12 = "../../../../results/robot/Combination12.txt"
gp_path_to_file_string_Combination12 = "../../../../results/string/Combination12.txt"

gp_result_parser_pixel_Combination12 = ResultParser(gp_path_to_file_pixel_Combination12)
gp_result_parser_robot_Combination12 = ResultParser(gp_path_to_file_robot_Combination12)
gp_result_parser_string_Combination12 = ResultParser(gp_path_to_file_string_Combination12)


def plot_error_progression(domain, example_name):
    initial_error = 0.0

    gp_cost_per_iteration_VanillaGP = []
    if (domain == "pixel"):
        initial_error = gp_result_parser_pixel_VanillaGP.get_initial_error(example_name)
        gp_cost_per_iteration_VanillaGP = gp_result_parser_pixel_VanillaGP.error_progression(example_name)
    elif (domain == "robot"):
        initial_error = gp_result_parser_robot_VanillaGP.get_initial_error(example_name)
        gp_cost_per_iteration_VanillaGP = gp_result_parser_robot_VanillaGP.error_progression(example_name)
    elif (domain == "string"):
        initial_error = gp_result_parser_string_VanillaGP.get_initial_error(example_name)
        gp_cost_per_iteration_VanillaGP = gp_result_parser_string_VanillaGP.error_progression(example_name)

    initial_error_line = [(i, initial_error) for i in [*range(0, len(gp_cost_per_iteration_VanillaGP))]]

    gp_cost_per_iteration_Brute = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Brute = gp_result_parser_pixel_Brute.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Brute = gp_result_parser_robot_Brute.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Brute = gp_result_parser_string_Brute.error_progression(example_name)

    gp_cost_per_iteration_Combination1 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination1 = gp_result_parser_pixel_Combination1.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination1 = gp_result_parser_robot_Combination1.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination1= gp_result_parser_string_Combination1.error_progression(example_name)

    gp_cost_per_iteration_Combination2 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination2 = gp_result_parser_pixel_Combination2.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination2 = gp_result_parser_robot_Combination2.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination2 = gp_result_parser_string_Combination2.error_progression(example_name)

    gp_cost_per_iteration_Combination3 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination3 = gp_result_parser_pixel_Combination3.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination3 = gp_result_parser_robot_Combination3.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination3 = gp_result_parser_string_Combination3.error_progression(example_name)

    gp_cost_per_iteration_Combination4 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination4 = gp_result_parser_pixel_Combination4.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination4 = gp_result_parser_robot_Combination4.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination4 = gp_result_parser_string_Combination4.error_progression(example_name)

    gp_cost_per_iteration_Combination5 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination5 = gp_result_parser_pixel_Combination5.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination5 = gp_result_parser_robot_Combination5.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination5 = gp_result_parser_string_Combination5.error_progression(example_name)

    gp_cost_per_iteration_Combination6 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination6 = gp_result_parser_pixel_Combination6.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination6 = gp_result_parser_robot_Combination6.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination6 = gp_result_parser_string_Combination6.error_progression(example_name)

    gp_cost_per_iteration_Combination7 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination7 = gp_result_parser_pixel_Combination7.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination7 = gp_result_parser_robot_Combination7.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination7 = gp_result_parser_string_Combination7.error_progression(example_name)

    gp_cost_per_iteration_Combination8 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination8 = gp_result_parser_pixel_Combination8.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination8 = gp_result_parser_robot_Combination8.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination8 = gp_result_parser_string_Combination8.error_progression(example_name)

    gp_cost_per_iteration_Combination9 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination9 = gp_result_parser_pixel_Combination9.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination9 = gp_result_parser_robot_Combination9.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination9 = gp_result_parser_string_Combination9.error_progression(example_name)

    gp_cost_per_iteration_Combination10 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination10 = gp_result_parser_pixel_Combination10.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination10 = gp_result_parser_robot_Combination10.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination10 = gp_result_parser_string_Combination10.error_progression(example_name)

    gp_cost_per_iteration_Combination11 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination11 = gp_result_parser_pixel_Combination11.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination11 = gp_result_parser_robot_Combination11.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination11 = gp_result_parser_string_Combination11.error_progression(example_name)

    gp_cost_per_iteration_Combination12 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination12 = gp_result_parser_pixel_Combination12.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination12 = gp_result_parser_robot_Combination12.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination12 = gp_result_parser_string_Combination12.error_progression(example_name)

    fig, ax = plt.subplots()
    ax.plot(*zip(*gp_cost_per_iteration_Brute), label="Original VanillaGP", color="midnightBlue")
    ax.plot(*zip(*gp_cost_per_iteration_VanillaGP), label="VanillaGP", color="mediumseagreen")
    ax.plot(*zip(*gp_cost_per_iteration_Combination1), label="Combination 1", color="mediumpurple")
    ax.plot(*zip(*gp_cost_per_iteration_Combination2), label="Combination 2", color="orangered")
    ax.plot(*zip(*gp_cost_per_iteration_Combination3), label="Combination 3", color="gold")
    ax.plot(*zip(*gp_cost_per_iteration_Combination4), label="Combination 4", color="slategrey")
    ax.plot(*zip(*gp_cost_per_iteration_Combination5), label="Combination 5", color="deepPink")
    ax.plot(*zip(*gp_cost_per_iteration_Combination6), label="Combination 6", color="peru")
    ax.plot(*zip(*gp_cost_per_iteration_Combination7), label="Combination 7", color="orangered")
    ax.plot(*zip(*gp_cost_per_iteration_Combination8), label="Combination 8", color="gold")
    ax.plot(*zip(*gp_cost_per_iteration_Combination9), label="Combination 9", color="slategrey")
    ax.plot(*zip(*gp_cost_per_iteration_Combination10), label="Combination 10", color="deepPink")
    ax.plot(*zip(*gp_cost_per_iteration_Combination11), label="Combination 11", color="peru")
    ax.plot(*zip(*gp_cost_per_iteration_Combination12), label="Combination 12", color="peru")
    ax.plot(*zip(*initial_error_line), label="Initial Error", color="black")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Error")
    ax.legend()
    ax.set_title("Error Progression in Example {}".format(example_name))

    plt.savefig("plots/error_progression_combination.svg")
    fig.clf()
    plt.close


def plot_complexity_vs_solved_percentage():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(17, 4))

    # Pixel
    domain = "pixel"
    gp_solved_percentage_Brute = gp_result_parser_pixel_Brute.solved_percentage_by_complexity(domain)
    gp_solved_percentage_VanillaGP = gp_result_parser_pixel_VanillaGP.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination1 = gp_result_parser_pixel_Combination1.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination2 = gp_result_parser_pixel_Combination2.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination3 = gp_result_parser_pixel_Combination3.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination4 = gp_result_parser_pixel_Combination4.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination5 = gp_result_parser_pixel_Combination5.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination6 = gp_result_parser_pixel_Combination6.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination7 = gp_result_parser_pixel_Combination7.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination8 = gp_result_parser_pixel_Combination8.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination9 = gp_result_parser_pixel_Combination9.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination10 = gp_result_parser_pixel_Combination10.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination11 = gp_result_parser_pixel_Combination11.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination12 = gp_result_parser_pixel_Combination12.solved_percentage_by_complexity(domain)

    ax1.plot(gp_solved_percentage_Brute.keys(), gp_solved_percentage_Brute.values(), label="Brute", color="midnightBlue", marker="o")
    ax1.plot(gp_solved_percentage_VanillaGP.keys(), gp_solved_percentage_VanillaGP.values(), label="VanillaGP", color="mediumseagreen", marker="^")
    ax1.plot(gp_solved_percentage_Combination1.keys(), gp_solved_percentage_Combination1.values(), label="Combination 1", color="mediumpurple", marker="o")
    ax1.plot(gp_solved_percentage_Combination2.keys(), gp_solved_percentage_Combination2.values(), label="Combination 2", color="orangered", marker="^")
    ax1.plot(gp_solved_percentage_Combination3.keys(), gp_solved_percentage_Combination3.values(), label="Combination 3", color="gold", marker="o")
    ax1.plot(gp_solved_percentage_Combination4.keys(), gp_solved_percentage_Combination4.values(), label="Combination 4", color="slategrey", marker="^")
    ax1.plot(gp_solved_percentage_Combination5.keys(), gp_solved_percentage_Combination5.values(), label="Combination 5", color="deepPink", marker="o")
    ax1.plot(gp_solved_percentage_Combination6.keys(), gp_solved_percentage_Combination6.values(), label="Combination 6", color="peru", marker="^")
    ax1.plot(gp_solved_percentage_Combination7.keys(), gp_solved_percentage_Combination7.values(), label="Combination 7", color="orangered", marker="o")
    ax1.plot(gp_solved_percentage_Combination8.keys(), gp_solved_percentage_Combination8.values(), label="Combination 8", color="gold", marker="^")
    ax1.plot(gp_solved_percentage_Combination9.keys(), gp_solved_percentage_Combination9.values(), label="Combination 9", color="slategrey", marker="o")
    ax1.plot(gp_solved_percentage_Combination10.keys(), gp_solved_percentage_Combination10.values(), label="Combination 10", color="deepPink", marker="^")
    ax1.plot(gp_solved_percentage_Combination11.keys(), gp_solved_percentage_Combination11.values(), label="Combination 11", color="peru", marker="o")
    ax1.plot(gp_solved_percentage_Combination12.keys(), gp_solved_percentage_Combination12.values(), label="Combination 12", color="peru", marker="^")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Tasks Solved (%)")
    ax1.set_title("Pixel Domain")
    ax1.set_box_aspect(1)

    # Robot
    domain = "robot"
    gp_solved_percentage_Brute = gp_result_parser_robot_Brute.solved_percentage_by_complexity(domain)
    gp_solved_percentage_VanillaGP = gp_result_parser_robot_VanillaGP.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination1 = gp_result_parser_robot_Combination1.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination2 = gp_result_parser_robot_Combination2.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination3 = gp_result_parser_robot_Combination3.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination4 = gp_result_parser_robot_Combination4.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination5 = gp_result_parser_robot_Combination5.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination6 = gp_result_parser_robot_Combination6.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination7 = gp_result_parser_robot_Combination7.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination8 = gp_result_parser_robot_Combination8.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination9 = gp_result_parser_robot_Combination9.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination10 = gp_result_parser_robot_Combination10.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination11 = gp_result_parser_robot_Combination11.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination12 = gp_result_parser_robot_Combination12.solved_percentage_by_complexity(domain)

    ax2.plot(gp_solved_percentage_Brute.keys(), gp_solved_percentage_Brute.values(), label="Brute", color="midnightBlue", marker="o")
    ax2.plot(gp_solved_percentage_VanillaGP.keys(), gp_solved_percentage_VanillaGP.values(), label="VanillaGP", color="mediumseagreen", marker="^")
    ax2.plot(gp_solved_percentage_Combination1.keys(), gp_solved_percentage_Combination1.values(), label="Combination 1", color="mediumpurple", marker="o")
    ax2.plot(gp_solved_percentage_Combination2.keys(), gp_solved_percentage_Combination2.values(), label="Combination 2", color="orangered", marker="^")
    ax2.plot(gp_solved_percentage_Combination3.keys(), gp_solved_percentage_Combination3.values(), label="Combination 3", color="gold", marker="o")
    ax2.plot(gp_solved_percentage_Combination4.keys(), gp_solved_percentage_Combination4.values(), label="Combination 4", color="slategrey", marker="^")
    ax2.plot(gp_solved_percentage_Combination5.keys(), gp_solved_percentage_Combination5.values(), label="Combination 5", color="deepPink", marker="o")
    ax2.plot(gp_solved_percentage_Combination6.keys(), gp_solved_percentage_Combination6.values(), label="Combination 6", color="peru", marker="^")
    ax2.plot(gp_solved_percentage_Combination7.keys(), gp_solved_percentage_Combination7.values(), label="Combination 7", color="tomato", marker="o")
    ax2.plot(gp_solved_percentage_Combination8.keys(), gp_solved_percentage_Combination8.values(), label="Combination 8", color="silver", marker="^")
    ax2.plot(gp_solved_percentage_Combination9.keys(), gp_solved_percentage_Combination9.values(), label="Combination 9", color="cornflowerblue", marker="o")
    ax2.plot(gp_solved_percentage_Combination10.keys(), gp_solved_percentage_Combination10.values(), label="Combination 10", color="black", marker="^")
    ax2.plot(gp_solved_percentage_Combination11.keys(), gp_solved_percentage_Combination11.values(), label="Combination 11", color="seagreen", marker="o")
    ax2.plot(gp_solved_percentage_Combination12.keys(), gp_solved_percentage_Combination12.values(), label="Combination 12", color="darkmagenta", marker="^")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Tasks Solved (%)")
    ax2.set_title("Robot Domain")
    ax2.set_box_aspect(1)

    # String
    domain = "string"
    gp_solved_percentage_Brute = gp_result_parser_string_Brute.solved_percentage_by_complexity(domain)
    gp_solved_percentage_VanillaGP = gp_result_parser_string_VanillaGP.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination1 = gp_result_parser_string_Combination1.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination2 = gp_result_parser_string_Combination2.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination3 = gp_result_parser_string_Combination3.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination4 = gp_result_parser_string_Combination4.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination5 = gp_result_parser_string_Combination5.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination6 = gp_result_parser_string_Combination6.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination7 = gp_result_parser_string_Combination7.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination8 = gp_result_parser_string_Combination8.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination9 = gp_result_parser_string_Combination9.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination10 = gp_result_parser_string_Combination10.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination11 = gp_result_parser_string_Combination11.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination12 = gp_result_parser_string_Combination12.solved_percentage_by_complexity(domain)

    ax3.plot(gp_solved_percentage_Brute.keys(), gp_solved_percentage_Brute.values(), label="Brute", color="midnightBlue", marker="o")
    ax3.plot(gp_solved_percentage_VanillaGP.keys(), gp_solved_percentage_VanillaGP.values(), label="VanillaGP", color="mediumseagreen", marker="^")
    ax3.plot(gp_solved_percentage_Combination1.keys(), gp_solved_percentage_Combination1.values(), label="Combination 1", color="mediumpurple", marker="o")
    ax3.plot(gp_solved_percentage_Combination2.keys(), gp_solved_percentage_Combination2.values(), label="Combination 2", color="orangered", marker="^")
    ax3.plot(gp_solved_percentage_Combination3.keys(), gp_solved_percentage_Combination3.values(), label="Combination 3", color="gold", marker="o")
    ax3.plot(gp_solved_percentage_Combination4.keys(), gp_solved_percentage_Combination4.values(), label="Combination 4", color="slategrey", marker="^")
    ax3.plot(gp_solved_percentage_Combination5.keys(), gp_solved_percentage_Combination5.values(), label="Combination 5", color="deepPink", marker="o")
    ax3.plot(gp_solved_percentage_Combination6.keys(), gp_solved_percentage_Combination6.values(), label="Combination 6", color="peru", marker="^")
    ax3.plot(gp_solved_percentage_Combination7.keys(), gp_solved_percentage_Combination7.values(), label="Combination 7", color="tomato", marker="o")
    ax3.plot(gp_solved_percentage_Combination8.keys(), gp_solved_percentage_Combination8.values(), label="Combination 8", color="silver", marker="^")
    ax3.plot(gp_solved_percentage_Combination9.keys(), gp_solved_percentage_Combination9.values(), label="Combination 9", color="cornflowerblue", marker="o")
    ax3.plot(gp_solved_percentage_Combination10.keys(), gp_solved_percentage_Combination10.values(), label="Combination 10", color="black", marker="^")
    ax3.plot(gp_solved_percentage_Combination11.keys(), gp_solved_percentage_Combination11.values(), label="Combination 11", color="seagreen", marker="o")
    ax3.plot(gp_solved_percentage_Combination12.keys(), gp_solved_percentage_Combination12.values(), label="Combination 12", color="darkmagenta", marker="^")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Tasks Solved (%)")
    ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax3.set_title("String Domain")
    ax3.set_box_aspect(1)

    plt.savefig("plots/solved_percentage_combination.svg")
    fig.clf()
    plt.close

def plot_complexity_vs_avg_test_cost():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

    # Pixel
    domain = "pixel"
    gp_avg_test_cost_Brute = gp_result_parser_pixel_Brute.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_VanillaGP = gp_result_parser_pixel_VanillaGP.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination1 = gp_result_parser_pixel_Combination1.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination2 = gp_result_parser_pixel_Combination2.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination3 = gp_result_parser_pixel_Combination3.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination4 = gp_result_parser_pixel_Combination4.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination5 = gp_result_parser_pixel_Combination5.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination6 = gp_result_parser_pixel_Combination6.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination7 = gp_result_parser_pixel_Combination7.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination8 = gp_result_parser_pixel_Combination8.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination9 = gp_result_parser_pixel_Combination9.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination10 = gp_result_parser_pixel_Combination10.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination11 = gp_result_parser_pixel_Combination11.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination12 = gp_result_parser_pixel_Combination12.avg_test_cost_by_complexity(domain)

    ax1.plot(gp_avg_test_cost_Brute.keys(), gp_avg_test_cost_Brute.values(), label="One-Point", color="midnightBlue", marker="o")
    ax1.plot(gp_avg_test_cost_VanillaGP.keys(), gp_avg_test_cost_VanillaGP.values(), label="VanillaGP", color="mediumseagreen", marker="^")
    ax1.plot(gp_avg_test_cost_Combination1.keys(), gp_avg_test_cost_Combination1.values(), label="Combination 1", color="mediumpurple", marker="o")
    ax1.plot(gp_avg_test_cost_Combination2.keys(), gp_avg_test_cost_Combination2.values(), label="Combination 2", color="orangered", marker="^")
    ax1.plot(gp_avg_test_cost_Combination3.keys(), gp_avg_test_cost_Combination3.values(), label="Combination 3", color="gold", marker="o")
    ax1.plot(gp_avg_test_cost_Combination4.keys(), gp_avg_test_cost_Combination4.values(), label="Combination 4", color="slategrey", marker="^")
    ax1.plot(gp_avg_test_cost_Combination5.keys(), gp_avg_test_cost_Combination5.values(), label="Combination 5", color="deepPink", marker="o")
    ax1.plot(gp_avg_test_cost_Combination6.keys(), gp_avg_test_cost_Combination6.values(), label="Combination 6", color="peru", marker="^")
    ax1.plot(gp_avg_test_cost_Combination7.keys(), gp_avg_test_cost_Combination7.values(), label="Combination 7", color="tomato", marker="o")
    ax1.plot(gp_avg_test_cost_Combination8.keys(), gp_avg_test_cost_Combination8.values(), label="Combination 8", color="silver", marker="^")
    ax1.plot(gp_avg_test_cost_Combination9.keys(), gp_avg_test_cost_Combination9.values(), label="Combination 9", color="cornflowerblue", marker="o")
    ax1.plot(gp_avg_test_cost_Combination10.keys(), gp_avg_test_cost_Combination10.values(), label="Combination 10", color="black", marker="^")
    ax1.plot(gp_avg_test_cost_Combination11.keys(), gp_avg_test_cost_Combination11.values(), label="Combination 11", color="seagreen", marker="o")
    ax1.plot(gp_avg_test_cost_Combination12.keys(), gp_avg_test_cost_Combination12.values(), label="Combination 12", color="darkmagenta", marker="^")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Average Test-Cost")
    ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_avg_test_cost_Brute = gp_result_parser_robot_Brute.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_VanillaGP = gp_result_parser_robot_VanillaGP.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination1 = gp_result_parser_robot_Combination1.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination2 = gp_result_parser_robot_Combination2.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination3 = gp_result_parser_robot_Combination3.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination4 = gp_result_parser_robot_Combination4.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination5 = gp_result_parser_robot_Combination5.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination6 = gp_result_parser_robot_Combination6.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination7 = gp_result_parser_robot_Combination7.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination8 = gp_result_parser_robot_Combination8.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination9 = gp_result_parser_robot_Combination9.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination10 = gp_result_parser_robot_Combination10.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination11 = gp_result_parser_robot_Combination11.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination12 = gp_result_parser_robot_Combination12.avg_test_cost_by_complexity(domain)

    ax2.plot(gp_avg_test_cost_Brute.keys(), gp_avg_test_cost_Brute.values(), label="Brute", color="midnightBlue", marker="o")
    ax2.plot(gp_avg_test_cost_VanillaGP.keys(), gp_avg_test_cost_VanillaGP.values(), label="VanillaGP", color="mediumseagreen", marker="^")
    ax2.plot(gp_avg_test_cost_Combination1.keys(), gp_avg_test_cost_Combination1.values(), label="Combination 1", color="mediumpurple", marker="o")
    ax2.plot(gp_avg_test_cost_Combination2.keys(), gp_avg_test_cost_Combination2.values(), label="Combination 2", color="orangered", marker="^")
    ax2.plot(gp_avg_test_cost_Combination3.keys(), gp_avg_test_cost_Combination3.values(), label="Combination 3", color="gold", marker="o")
    ax2.plot(gp_avg_test_cost_Combination4.keys(), gp_avg_test_cost_Combination4.values(), label="Combination 4", color="slategrey", marker="^")
    ax2.plot(gp_avg_test_cost_Combination5.keys(), gp_avg_test_cost_Combination5.values(), label="Combination 5", color="deepPink", marker="o")
    ax2.plot(gp_avg_test_cost_Combination6.keys(), gp_avg_test_cost_Combination6.values(), label="Combination 6", color="peru", marker="^")
    ax2.plot(gp_avg_test_cost_Combination7.keys(), gp_avg_test_cost_Combination7.values(), label="Combination 7", color="tomato", marker="o")
    ax2.plot(gp_avg_test_cost_Combination8.keys(), gp_avg_test_cost_Combination8.values(), label="Combination 8", color="silver", marker="^")
    ax2.plot(gp_avg_test_cost_Combination9.keys(), gp_avg_test_cost_Combination9.values(), label="Combination 9", color="cornflowerblue", marker="o")
    ax2.plot(gp_avg_test_cost_Combination10.keys(), gp_avg_test_cost_Combination10.values(), label="Combination 10", color="black", marker="^")
    ax2.plot(gp_avg_test_cost_Combination11.keys(), gp_avg_test_cost_Combination11.values(), label="Combination 11", color="seagreen", marker="o")
    ax2.plot(gp_avg_test_cost_Combination12.keys(), gp_avg_test_cost_Combination12.values(), label="Combination 12", color="darkmagenta", marker="^")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Average Test-Cost")
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_avg_test_cost_Brute = gp_result_parser_string_Brute.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_VanillaGP = gp_result_parser_string_VanillaGP.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination1 = gp_result_parser_string_Combination1.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination2 = gp_result_parser_string_Combination2.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination3 = gp_result_parser_string_Combination3.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination4 = gp_result_parser_string_Combination4.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination5 = gp_result_parser_string_Combination5.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination6 = gp_result_parser_string_Combination6.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination7 = gp_result_parser_string_Combination7.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination8 = gp_result_parser_string_Combination8.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination9 = gp_result_parser_string_Combination9.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination10 = gp_result_parser_string_Combination10.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination11 = gp_result_parser_string_Combination11.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination12 = gp_result_parser_string_Combination12.avg_test_cost_by_complexity(domain)

    ax3.plot(gp_avg_test_cost_Brute.keys(), gp_avg_test_cost_Brute.values(), label="Brute", color="midnightBlue", marker="o")
    ax3.plot(gp_avg_test_cost_VanillaGP.keys(), gp_avg_test_cost_VanillaGP.values(), label="VanillaGP", color="mediumseagreen", marker="^")
    ax3.plot(gp_avg_test_cost_Combination1.keys(), gp_avg_test_cost_Combination1.values(), label="Combination 1", color="mediumpurple", marker="o")
    ax3.plot(gp_avg_test_cost_Combination2.keys(), gp_avg_test_cost_Combination2.values(), label="Combination 2", color="orangered", marker="^")
    ax3.plot(gp_avg_test_cost_Combination3.keys(), gp_avg_test_cost_Combination3.values(), label="Combination 3", color="gold", marker="o")
    ax3.plot(gp_avg_test_cost_Combination4.keys(), gp_avg_test_cost_Combination4.values(), label="Combination 4", color="slategrey", marker="^")
    ax3.plot(gp_avg_test_cost_Combination5.keys(), gp_avg_test_cost_Combination5.values(), label="Combination 5", color="deepPink", marker="o")
    ax3.plot(gp_avg_test_cost_Combination6.keys(), gp_avg_test_cost_Combination6.values(), label="Combination 6", color="peru", marker="^")
    ax3.plot(gp_avg_test_cost_Combination7.keys(), gp_avg_test_cost_Combination7.values(), label="Combination 7", color="tomato", marker="o")
    ax3.plot(gp_avg_test_cost_Combination8.keys(), gp_avg_test_cost_Combination8.values(), label="Combination 8", color="silver", marker="^")
    ax3.plot(gp_avg_test_cost_Combination9.keys(), gp_avg_test_cost_Combination9.values(), label="Combination 9", color="cornflowerblue", marker="o")
    ax3.plot(gp_avg_test_cost_Combination10.keys(), gp_avg_test_cost_Combination10.values(), label="Combination 10", color="black", marker="^")
    ax3.plot(gp_avg_test_cost_Combination11.keys(), gp_avg_test_cost_Combination11.values(), label="Combination 11", color="seagreen", marker="o")
    ax3.plot(gp_avg_test_cost_Combination12.keys(), gp_avg_test_cost_Combination12.values(), label="Combination 12", color="darkmagenta", marker="^")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Average Test-Cost")
    ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax3.set_title("String Domain")

    plt.savefig("plots/avg_test_cost_combination.svg")
    fig.clf()
    plt.close

def plot_rel_improvement():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

    # Pixel
    domain = "pixel"
    gp_avg_rel_improvement_Brute = gp_result_parser_pixel_Brute.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_VanillaGP = gp_result_parser_pixel_VanillaGP.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination1 = gp_result_parser_pixel_Combination1.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination2 = gp_result_parser_pixel_Combination2.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination3 = gp_result_parser_pixel_Combination3.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination4 = gp_result_parser_pixel_Combination4.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination5 = gp_result_parser_pixel_Combination5.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination6 = gp_result_parser_pixel_Combination6.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination7 = gp_result_parser_pixel_Combination7.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination8 = gp_result_parser_pixel_Combination8.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination9 = gp_result_parser_pixel_Combination9.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination10 = gp_result_parser_pixel_Combination10.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination11 = gp_result_parser_pixel_Combination11.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination12 = gp_result_parser_pixel_Combination12.rel_improvement_by_complexity(domain)

    ax1.plot(gp_avg_rel_improvement_Brute.keys(), gp_avg_rel_improvement_Brute.values(), label="Brute", color="midnightBlue",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_VanillaGP.keys(), gp_avg_rel_improvement_VanillaGP.values(), label="VanillaGP", color="mediumseagreen",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_Combination1.keys(), gp_avg_rel_improvement_Combination1.values(), label="Combination 1",
             color="mediumpurple",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_Combination2.keys(), gp_avg_rel_improvement_Combination2.values(), label="Combination 2",
             color="orangered",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_Combination3.keys(), gp_avg_rel_improvement_Combination3.values(), label="Combination 3",
             color="gold",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_Combination4.keys(), gp_avg_rel_improvement_Combination4.values(), label="Combination 4",
             color="slategrey",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_Combination5.keys(), gp_avg_rel_improvement_Combination5.values(), label="Combination 5",
             color="deepPink",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_Combination6.keys(), gp_avg_rel_improvement_Combination6.values(), label="Combination 6",
             color="peru",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_Combination7.keys(), gp_avg_rel_improvement_Combination7.values(), label="Combination 7",
             color="tomato",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_Combination8.keys(), gp_avg_rel_improvement_Combination8.values(), label="Combination 8",
             color="silver",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_Combination9.keys(), gp_avg_rel_improvement_Combination9.values(), label="Combination 9",
             color="cornflowerblue",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_Combination10.keys(), gp_avg_rel_improvement_Combination10.values(), label="Combination 10",
             color="black",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_Combination11.keys(), gp_avg_rel_improvement_Combination11.values(), label="Combination 11",
             color="seagreen",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_Combination12.keys(), gp_avg_rel_improvement_Combination12.values(), label="Combination 12",
             color="darkmagenta",
             marker="^")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Avg. Relative Improvement (%)")
    ax1.set_ylim(ymin=0)
    ax1.legend()
    ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_avg_rel_improvement_Brute = gp_result_parser_robot_Brute.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_VanillaGP = gp_result_parser_robot_VanillaGP.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination1 = gp_result_parser_robot_Combination1.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination2 = gp_result_parser_robot_Combination2.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination3 = gp_result_parser_robot_Combination3.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination4 = gp_result_parser_robot_Combination4.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination5 = gp_result_parser_robot_Combination5.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination6 = gp_result_parser_robot_Combination6.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination7 = gp_result_parser_robot_Combination7.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination8 = gp_result_parser_robot_Combination8.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination9 = gp_result_parser_robot_Combination9.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination10 = gp_result_parser_robot_Combination10.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination11 = gp_result_parser_robot_Combination11.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination12 = gp_result_parser_robot_Combination12.rel_improvement_by_complexity(domain)

    ax2.plot(gp_avg_rel_improvement_Brute.keys(), gp_avg_rel_improvement_Brute.values(), label="Brute", color="midnightBlue",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_VanillaGP.keys(), gp_avg_rel_improvement_VanillaGP.values(), label="VanillaGP", color="mediumseagreen",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_Combination1.keys(), gp_avg_rel_improvement_Combination1.values(), label="Combination 1",
             color="mediumpurple",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_Combination2.keys(), gp_avg_rel_improvement_Combination2.values(), label="Combination 2",
             color="orangered",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_Combination3.keys(), gp_avg_rel_improvement_Combination3.values(), label="Combination 3",
             color="gold",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_Combination4.keys(), gp_avg_rel_improvement_Combination4.values(), label="Combination 4",
             color="slategrey",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_Combination5.keys(), gp_avg_rel_improvement_Combination5.values(), label="Combination 5",
             color="deepPink",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_Combination6.keys(), gp_avg_rel_improvement_Combination6.values(), label="Combination 6",
             color="peru",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_Combination7.keys(), gp_avg_rel_improvement_Combination7.values(), label="Combination 7",
             color="tomato",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_Combination8.keys(), gp_avg_rel_improvement_Combination8.values(), label="Combination 8",
             color="silver",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_Combination9.keys(), gp_avg_rel_improvement_Combination9.values(), label="Combination 9",
             color="cornflowerblue",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_Combination10.keys(), gp_avg_rel_improvement_Combination10.values(), label="Combination 10",
             color="black",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_Combination11.keys(), gp_avg_rel_improvement_Combination11.values(), label="Combination 11",
             color="seagreen",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_Combination12.keys(), gp_avg_rel_improvement_Combination12.values(), label="Combination 12",
             color="darkmagenta",
             marker="^")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Avg. Relative Improvement (%)")
    ax2.set_ylim(ymin=0)
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_avg_rel_improvement_Brute = gp_result_parser_string_Brute.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_VanillaGP = gp_result_parser_string_VanillaGP.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination1 = gp_result_parser_string_Combination1.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination2 = gp_result_parser_string_Combination2.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination3 = gp_result_parser_string_Combination3.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination4 = gp_result_parser_string_Combination4.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination5 = gp_result_parser_string_Combination5.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination6 = gp_result_parser_string_Combination6.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination7 = gp_result_parser_string_Combination7.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination8 = gp_result_parser_string_Combination8.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination9 = gp_result_parser_string_Combination9.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination10 = gp_result_parser_string_Combination10.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination11 = gp_result_parser_string_Combination11.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination12 = gp_result_parser_string_Combination12.rel_improvement_by_complexity(domain)

    ax3.plot(gp_avg_rel_improvement_Brute.keys(), gp_avg_rel_improvement_Brute.values(), label="Brute", color="midnightBlue",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_VanillaGP.keys(), gp_avg_rel_improvement_VanillaGP.values(), label="VanillaGP", color="mediumseagreen",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_Combination1.keys(), gp_avg_rel_improvement_Combination1.values(), label="Combination 1",
             color="mediumpurple",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_Combination2.keys(), gp_avg_rel_improvement_Combination2.values(), label="Combination 2",
             color="orangered",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_Combination3.keys(), gp_avg_rel_improvement_Combination3.values(), label="Combination 3",
             color="gold",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_Combination4.keys(), gp_avg_rel_improvement_Combination4.values(), label="Combination 4",
             color="slategrey",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_Combination5.keys(), gp_avg_rel_improvement_Combination5.values(), label="Combination 5",
             color="deepPink",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_Combination6.keys(), gp_avg_rel_improvement_Combination6.values(), label="Combination 6",
             color="peru",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_Combination7.keys(), gp_avg_rel_improvement_Combination7.values(), label="Combination 7",
             color="tomato",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_Combination8.keys(), gp_avg_rel_improvement_Combination8.values(), label="Combination 8",
             color="silver",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_Combination9.keys(), gp_avg_rel_improvement_Combination9.values(), label="Combination 9",
             color="cornflowerblue",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_Combination10.keys(), gp_avg_rel_improvement_Combination10.values(), label="Combination 10",
             color="black",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_Combination11.keys(), gp_avg_rel_improvement_Combination11.values(), label="Combination 11",
             color="seagreen",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_Combination12.keys(), gp_avg_rel_improvement_Combination12.values(), label="Combination 12",
             color="darkmagenta",
             marker="^")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Avg. Relative Improvement (%)")
    ax3.set_ylim(ymin=0)
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/relative_improvement_combination.svg")
    fig.clf()
    plt.close

def plot_dis_to_correct():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

# plot_rel_improvement()
plot_complexity_vs_solved_percentage()
plot_error_progression("string", "strings/1-58-1.pl")
plot_complexity_vs_avg_test_cost()
