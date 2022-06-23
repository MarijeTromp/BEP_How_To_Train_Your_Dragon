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

# AlteredOneMutationLoops25
gp_path_to_file_pixel_AlteredOneMutationLoops25 = "../../../../results/pixel/AlteredOneMutationLoops25.txt"
gp_path_to_file_robot_AlteredOneMutationLoops25 = "../../../../results/robot/AlteredOneMutationLoops25.txt"
gp_path_to_file_string_AlteredOneMutationLoops25 = "../../../../results/string/AlteredOneMutationLoops25.txt"

gp_result_parser_pixel_AlteredOneMutationLoops25 = ResultParser(gp_path_to_file_pixel_AlteredOneMutationLoops25)
gp_result_parser_robot_AlteredOneMutationLoops25 = ResultParser(gp_path_to_file_robot_AlteredOneMutationLoops25)
gp_result_parser_string_AlteredOneMutationLoops25 = ResultParser(gp_path_to_file_string_AlteredOneMutationLoops25)

# AlteredOneMutationLoops375
gp_path_to_file_pixel_AlteredOneMutationLoops375 = "../../../../results/pixel/AlteredOneMutationLoops375.txt"
gp_path_to_file_robot_AlteredOneMutationLoops375 = "../../../../results/robot/AlteredOneMutationLoops375.txt"
gp_path_to_file_string_AlteredOneMutationLoops375 = "../../../../results/string/AlteredOneMutationLoops375.txt"

gp_result_parser_pixel_AlteredOneMutationLoops375 = ResultParser(gp_path_to_file_pixel_AlteredOneMutationLoops375)
gp_result_parser_robot_AlteredOneMutationLoops375 = ResultParser(gp_path_to_file_robot_AlteredOneMutationLoops375)
gp_result_parser_string_AlteredOneMutationLoops375 = ResultParser(gp_path_to_file_string_AlteredOneMutationLoops375)

# AlteredOneMutationLoops50
gp_path_to_file_pixel_AlteredOneMutationLoops50 = "../../../../results/pixel/AlteredOneMutationLoops50.txt"
gp_path_to_file_robot_AlteredOneMutationLoops50 = "../../../../results/robot/AlteredOneMutationLoops50.txt"
gp_path_to_file_string_AlteredOneMutationLoops50 = "../../../../results/string/AlteredOneMutationLoops50.txt"

gp_result_parser_pixel_AlteredOneMutationLoops50 = ResultParser(gp_path_to_file_pixel_AlteredOneMutationLoops50)
gp_result_parser_robot_AlteredOneMutationLoops50 = ResultParser(gp_path_to_file_robot_AlteredOneMutationLoops50)
gp_result_parser_string_AlteredOneMutationLoops50 = ResultParser(gp_path_to_file_string_AlteredOneMutationLoops50)

# AlteredOneMutation
gp_path_to_file_pixel_AlteredOneMutation = "../../../../results/pixel/AlteredOneMutation.txt"
gp_path_to_file_robot_AlteredOneMutation = "../../../../results/robot/AlteredOneMutation.txt"
gp_path_to_file_string_AlteredOneMutation = "../../../../results/string/AlteredOneMutation.txt"

gp_result_parser_pixel_AlteredOneMutation = ResultParser(gp_path_to_file_pixel_AlteredOneMutation)
gp_result_parser_robot_AlteredOneMutation = ResultParser(gp_path_to_file_robot_AlteredOneMutation)
gp_result_parser_string_AlteredOneMutation = ResultParser(gp_path_to_file_string_AlteredOneMutation)

# Combination7
gp_path_to_file_pixel_Combination7 = "../../../../results/pixel/Combination7.txt"
gp_path_to_file_robot_Combination7 = "../../../../results/robot/Combination7.txt"
gp_path_to_file_string_Combination7 = "../../../../results/string/Combination7.txt"

gp_result_parser_pixel_Combination7 = ResultParser(gp_path_to_file_pixel_Combination7)
gp_result_parser_robot_Combination7 = ResultParser(gp_path_to_file_robot_Combination7)
gp_result_parser_string_Combination7 = ResultParser(gp_path_to_file_string_Combination7)

# Downsampled_ThreeParent_AlteredOneMutationLoops
gp_path_to_file_pixel_Downsampled_ThreeParent_AlteredOneMutationLoops = "../../../../results/pixel/Downsampled_ThreeParent_AlteredOneMutationLoops.txt"
gp_path_to_file_robot_Downsampled_ThreeParent_AlteredOneMutationLoops = "../../../../results/robot/Downsampled_ThreeParent_AlteredOneMutationLoops.txt"
gp_path_to_file_string_Downsampled_ThreeParent_AlteredOneMutationLoops = "../../../../results/string/Downsampled_ThreeParent_AlteredOneMutationLoops.txt"

gp_result_parser_pixel_Downsampled_ThreeParent_AlteredOneMutationLoops = ResultParser(gp_path_to_file_pixel_Downsampled_ThreeParent_AlteredOneMutationLoops)
gp_result_parser_robot_Downsampled_ThreeParent_AlteredOneMutationLoops = ResultParser(gp_path_to_file_robot_Downsampled_ThreeParent_AlteredOneMutationLoops)
gp_result_parser_string_Downsampled_ThreeParent_AlteredOneMutationLoops = ResultParser(gp_path_to_file_string_Downsampled_ThreeParent_AlteredOneMutationLoops)

# VanillaGP
gp_path_to_file_pixel_VanillaGP = "../../../../results/pixel/VanillaGP.txt"
gp_path_to_file_robot_VanillaGP = "../../../../results/robot/VanillaGP.txt"
gp_path_to_file_string_VanillaGP = "../../../../results/string/VanillaGP.txt"

gp_result_parser_pixel_VanillaGP = ResultParser(gp_path_to_file_pixel_VanillaGP)
gp_result_parser_robot_VanillaGP = ResultParser(gp_path_to_file_robot_VanillaGP)
gp_result_parser_string_VanillaGP = ResultParser(gp_path_to_file_string_VanillaGP)

def plot_error_progression(domain, example_name):
    initial_error = 0.0

    gp_cost_per_iteration_AlteredOneMutationLoops25 = []
    if (domain == "pixel"):
        initial_error = gp_result_parser_pixel_AlteredOneMutationLoops25.get_initial_error(example_name)
        gp_cost_per_iteration_AlteredOneMutationLoops25 = gp_result_parser_pixel_AlteredOneMutationLoops25.error_progression(example_name)
    elif (domain == "robot"):
        initial_error = gp_result_parser_robot_AlteredOneMutationLoops25.get_initial_error(example_name)
        gp_cost_per_iteration_AlteredOneMutationLoops25 = gp_result_parser_robot_AlteredOneMutationLoops25.error_progression(example_name)
    elif (domain == "string"):
        initial_error = gp_result_parser_string_AlteredOneMutationLoops25.get_initial_error(example_name)
        gp_cost_per_iteration_AlteredOneMutationLoops25 = gp_result_parser_string_AlteredOneMutationLoops25.error_progression(example_name)

    initial_error_line = [(i, initial_error) for i in [*range(0, len(gp_cost_per_iteration_AlteredOneMutationLoops25))]]

    gp_cost_per_iteration_Brute = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Brute = gp_result_parser_pixel_Brute.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Brute = gp_result_parser_robot_Brute.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Brute = gp_result_parser_string_Brute.error_progression(example_name)

    gp_cost_per_iteration_AlteredOneMutationLoops50 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_AlteredOneMutationLoops50 = gp_result_parser_pixel_AlteredOneMutationLoops50.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_AlteredOneMutationLoops50 = gp_result_parser_robot_AlteredOneMutationLoops50.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_AlteredOneMutationLoops50= gp_result_parser_string_AlteredOneMutationLoops50.error_progression(example_name)

    gp_cost_per_iteration_AlteredOneMutation = []
    if (domain == "pixel"):
        gp_cost_per_iteration_AlteredOneMutation = gp_result_parser_pixel_AlteredOneMutation.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_AlteredOneMutation = gp_result_parser_robot_AlteredOneMutation.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_AlteredOneMutation = gp_result_parser_string_AlteredOneMutation.error_progression(example_name)

    gp_cost_per_iteration_Combination7 = []
    if (domain == "pixel"):
        gp_cost_per_iteration_Combination7 = gp_result_parser_pixel_Combination7.error_progression(example_name)
    elif (domain == "robot"):
        gp_cost_per_iteration_Combination7 = gp_result_parser_robot_Combination7.error_progression(example_name)
    elif (domain == "string"):
        gp_cost_per_iteration_Combination7 = gp_result_parser_string_Combination7.error_progression(example_name)

    fig, ax = plt.subplots()
    ax.plot(*zip(*gp_cost_per_iteration_Brute), label="Brute", color="midnightBlue")
    ax.plot(*zip(*gp_cost_per_iteration_AlteredOneMutationLoops25), label="Loops 25%", color="mediumseagreen")
    ax.plot(*zip(*gp_cost_per_iteration_AlteredOneMutationLoops50), label="Loops 50%", color="mediumpurple")
    ax.plot(*zip(*gp_cost_per_iteration_AlteredOneMutation), label="Altered One Mutation", color="orangered")
    ax.plot(*zip(*gp_cost_per_iteration_Combination7), label="Combination 7", color="gold")
    ax.plot(*zip(*initial_error_line), label="Initial Error", color="black")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Error")
    ax.legend()
    ax.set_title("Error Progression in Example {}".format(example_name))

    plt.savefig("plots/error_progression_loops.svg")
    fig.clf()
    plt.close


def plot_complexity_vs_solved_percentage():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(17, 4))

    # Pixel
    domain = "pixel"
    gp_solved_percentage_VanillaGP = gp_result_parser_pixel_VanillaGP.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Brute = gp_result_parser_pixel_Brute.solved_percentage_by_complexity(domain)
    gp_solved_percentage_AlteredOneMutationLoops25 = gp_result_parser_pixel_AlteredOneMutationLoops25.solved_percentage_by_complexity(domain)
    gp_solved_percentage_AlteredOneMutationLoops50 = gp_result_parser_pixel_AlteredOneMutationLoops50.solved_percentage_by_complexity(domain)
    gp_solved_percentage_AlteredOneMutation = gp_result_parser_pixel_AlteredOneMutation.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination7 = gp_result_parser_pixel_Combination7.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Downsampled_ThreeParent_AlteredOneMutationLoops = gp_result_parser_pixel_Downsampled_ThreeParent_AlteredOneMutationLoops.solved_percentage_by_complexity(domain)

    ax1.plot(gp_solved_percentage_VanillaGP.keys(), gp_solved_percentage_VanillaGP.values(), label="VanillaGP",
             color="silver", marker="^")
    ax1.plot(gp_solved_percentage_Brute.keys(), gp_solved_percentage_Brute.values(), label="Brute", color="midnightBlue", marker="o")
    ax1.plot(gp_solved_percentage_AlteredOneMutationLoops25.keys(), gp_solved_percentage_AlteredOneMutationLoops25.values(), label="Loops 25%", color="mediumseagreen", marker="^")
    ax1.plot(gp_solved_percentage_AlteredOneMutationLoops50.keys(), gp_solved_percentage_AlteredOneMutationLoops50.values(), label="Loops 50%", color="mediumpurple", marker="o")
    ax1.plot(gp_solved_percentage_AlteredOneMutation.keys(), gp_solved_percentage_AlteredOneMutation.values(), label="Altered One Mutation", color="orangered", marker="^")
    ax1.plot(gp_solved_percentage_Combination7.keys(), gp_solved_percentage_Combination7.values(), label="Best combination string", color="gold", marker="o")
    ax1.plot(gp_solved_percentage_Downsampled_ThreeParent_AlteredOneMutationLoops.keys(), gp_solved_percentage_Downsampled_ThreeParent_AlteredOneMutationLoops.values(), label="Best combination other \n with loops 50%", color="cornflowerblue", marker="^")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Tasks Solved (%)")
    ax1.legend()
    ax1.set_title("ASCII Art Domain")

    # Robot
    domain = "robot"
    gp_solved_percentage_VanillaGP = gp_result_parser_robot_VanillaGP.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Brute = gp_result_parser_robot_Brute.solved_percentage_by_complexity(domain)
    gp_solved_percentage_AlteredOneMutationLoops25 = gp_result_parser_robot_AlteredOneMutationLoops25.solved_percentage_by_complexity(domain)
    gp_solved_percentage_AlteredOneMutationLoops50 = gp_result_parser_robot_AlteredOneMutationLoops50.solved_percentage_by_complexity(domain)
    gp_solved_percentage_AlteredOneMutation = gp_result_parser_robot_AlteredOneMutation.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination7 = gp_result_parser_robot_Combination7.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Downsampled_ThreeParent_AlteredOneMutationLoops = gp_result_parser_robot_Downsampled_ThreeParent_AlteredOneMutationLoops.solved_percentage_by_complexity(domain)

    ax2.plot(gp_solved_percentage_VanillaGP.keys(), gp_solved_percentage_VanillaGP.values(), label="VanillaGP", color="silver", marker="^")
    ax2.plot(gp_solved_percentage_Brute.keys(), gp_solved_percentage_Brute.values(), label="Brute", color="midnightBlue", marker="o")
    ax2.plot(gp_solved_percentage_AlteredOneMutationLoops25.keys(), gp_solved_percentage_AlteredOneMutationLoops25.values(), label="Loops 25", color="mediumseagreen", marker="^")
    ax2.plot(gp_solved_percentage_AlteredOneMutationLoops50.keys(), gp_solved_percentage_AlteredOneMutationLoops50.values(), label="Loops 50", color="mediumpurple", marker="o")
    ax2.plot(gp_solved_percentage_AlteredOneMutation.keys(), gp_solved_percentage_AlteredOneMutation.values(), label="Altered One Mutation", color="orangered", marker="^")
    ax2.plot(gp_solved_percentage_Combination7.keys(), gp_solved_percentage_Combination7.values(), label="Best combination string", color="gold", marker="o")
    ax2.plot(gp_solved_percentage_Downsampled_ThreeParent_AlteredOneMutationLoops.keys(), gp_solved_percentage_Downsampled_ThreeParent_AlteredOneMutationLoops.values(), label="Best combination other \n with loops 50%", color="cornflowerblue", marker="^")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Tasks Solved (%)")
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_solved_percentage_VanillaGP = gp_result_parser_string_VanillaGP.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Brute = gp_result_parser_string_Brute.solved_percentage_by_complexity(domain)
    gp_solved_percentage_AlteredOneMutationLoops25 = gp_result_parser_string_AlteredOneMutationLoops25.solved_percentage_by_complexity(domain)
    gp_solved_percentage_AlteredOneMutationLoops50 = gp_result_parser_string_AlteredOneMutationLoops50.solved_percentage_by_complexity(domain)
    gp_solved_percentage_AlteredOneMutation = gp_result_parser_string_AlteredOneMutation.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Combination7 = gp_result_parser_string_Combination7.solved_percentage_by_complexity(domain)
    gp_solved_percentage_Downsampled_ThreeParent_AlteredOneMutationLoops = gp_result_parser_string_Downsampled_ThreeParent_AlteredOneMutationLoops.solved_percentage_by_complexity(domain)

    ax3.plot(gp_solved_percentage_VanillaGP.keys(), gp_solved_percentage_VanillaGP.values(), label="VanillaGP", color="silver", marker="^")
    ax3.plot(gp_solved_percentage_Brute.keys(), gp_solved_percentage_Brute.values(), label="Brute", color="midnightBlue", marker="o")
    ax3.plot(gp_solved_percentage_AlteredOneMutationLoops25.keys(), gp_solved_percentage_AlteredOneMutationLoops25.values(), label="Loops 25", color="mediumseagreen", marker="^")
    ax3.plot(gp_solved_percentage_AlteredOneMutationLoops50.keys(), gp_solved_percentage_AlteredOneMutationLoops50.values(), label="Loops 50", color="mediumpurple", marker="o")
    ax3.plot(gp_solved_percentage_AlteredOneMutation.keys(), gp_solved_percentage_AlteredOneMutation.values(), label="Altered One Mutation", color="orangered", marker="^")
    ax3.plot(gp_solved_percentage_Combination7.keys(), gp_solved_percentage_Combination7.values(), label="Best combination string", color="gold", marker="o")
    ax3.plot(gp_solved_percentage_Downsampled_ThreeParent_AlteredOneMutationLoops.keys(), gp_solved_percentage_Downsampled_ThreeParent_AlteredOneMutationLoops.values(), label="Best combination other \n with loops 50%", color="cornflowerblue", marker="^")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Tasks Solved (%)")
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/solved_percentage_loops.svg")
    fig.clf()
    plt.close

def plot_complexity_vs_avg_test_cost():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(17, 4))

    # Pixel
    domain = "pixel"
    gp_avg_test_cost_Brute = gp_result_parser_pixel_Brute.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_AlteredOneMutationLoops25 = gp_result_parser_pixel_AlteredOneMutationLoops25.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_AlteredOneMutationLoops50 = gp_result_parser_pixel_AlteredOneMutationLoops50.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_AlteredOneMutation = gp_result_parser_pixel_AlteredOneMutation.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination7 = gp_result_parser_pixel_Combination7.avg_test_cost_by_complexity(domain)

    ax1.plot(gp_avg_test_cost_Brute.keys(), gp_avg_test_cost_Brute.values(), label="One-Point", color="midnightBlue", marker="o")
    ax1.plot(gp_avg_test_cost_AlteredOneMutationLoops25.keys(), gp_avg_test_cost_AlteredOneMutationLoops25.values(), label="Loops 25", color="mediumseagreen", marker="^")
    ax1.plot(gp_avg_test_cost_AlteredOneMutationLoops50.keys(), gp_avg_test_cost_AlteredOneMutationLoops50.values(), label="Loops 50", color="mediumpurple", marker="o")
    ax1.plot(gp_avg_test_cost_AlteredOneMutation.keys(), gp_avg_test_cost_AlteredOneMutation.values(), label="Altered One Mutation", color="orangered", marker="^")
    ax1.plot(gp_avg_test_cost_Combination7.keys(), gp_avg_test_cost_Combination7.values(), label="Combination 7", color="gold", marker="o")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Average Test-Cost")
    ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_avg_test_cost_Brute = gp_result_parser_robot_Brute.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_AlteredOneMutationLoops25 = gp_result_parser_robot_AlteredOneMutationLoops25.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_AlteredOneMutationLoops50 = gp_result_parser_robot_AlteredOneMutationLoops50.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_AlteredOneMutation = gp_result_parser_robot_AlteredOneMutation.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination7 = gp_result_parser_robot_Combination7.avg_test_cost_by_complexity(domain)

    ax2.plot(gp_avg_test_cost_Brute.keys(), gp_avg_test_cost_Brute.values(), label="Brute", color="midnightBlue", marker="o")
    ax2.plot(gp_avg_test_cost_AlteredOneMutationLoops25.keys(), gp_avg_test_cost_AlteredOneMutationLoops25.values(), label="Loops 25", color="mediumseagreen", marker="^")
    ax2.plot(gp_avg_test_cost_AlteredOneMutationLoops50.keys(), gp_avg_test_cost_AlteredOneMutationLoops50.values(), label="Loops 50", color="mediumpurple", marker="o")
    ax2.plot(gp_avg_test_cost_AlteredOneMutation.keys(), gp_avg_test_cost_AlteredOneMutation.values(), label="Altered One Mutation", color="orangered", marker="^")
    ax2.plot(gp_avg_test_cost_Combination7.keys(), gp_avg_test_cost_Combination7.values(), label="Combination 7", color="gold", marker="o")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Average Test-Cost")
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_avg_test_cost_Brute = gp_result_parser_string_Brute.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_AlteredOneMutationLoops25 = gp_result_parser_string_AlteredOneMutationLoops25.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_AlteredOneMutationLoops50 = gp_result_parser_string_AlteredOneMutationLoops50.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_AlteredOneMutation = gp_result_parser_string_AlteredOneMutation.avg_test_cost_by_complexity(domain)
    gp_avg_test_cost_Combination7 = gp_result_parser_string_Combination7.avg_test_cost_by_complexity(domain)
    ax3.plot(gp_avg_test_cost_Brute.keys(), gp_avg_test_cost_Brute.values(), label="Brute", color="midnightBlue", marker="o")
    ax3.plot(gp_avg_test_cost_AlteredOneMutationLoops25.keys(), gp_avg_test_cost_AlteredOneMutationLoops25.values(), label="Loops 25", color="mediumseagreen", marker="^")
    ax3.plot(gp_avg_test_cost_AlteredOneMutationLoops50.keys(), gp_avg_test_cost_AlteredOneMutationLoops50.values(), label="Loops 50", color="mediumpurple", marker="o")
    ax3.plot(gp_avg_test_cost_AlteredOneMutation.keys(), gp_avg_test_cost_AlteredOneMutation.values(), label="Altered One Mutation", color="orangered", marker="^")
    ax3.plot(gp_avg_test_cost_Combination7.keys(), gp_avg_test_cost_Combination7.values(), label="Combination 7", color="gold", marker="o")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Average Test-Cost")
    ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax3.set_title("String Domain")

    plt.savefig("plots/avg_test_cost_loops.svg")
    fig.clf()
    plt.close

def plot_rel_improvement():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

    # Pixel
    domain = "pixel"
    gp_avg_rel_improvement_Brute = gp_result_parser_pixel_Brute.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_AlteredOneMutationLoops25 = gp_result_parser_pixel_AlteredOneMutationLoops25.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_AlteredOneMutationLoops50 = gp_result_parser_pixel_AlteredOneMutationLoops50.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_AlteredOneMutation = gp_result_parser_pixel_AlteredOneMutation.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination7 = gp_result_parser_pixel_Combination7.rel_improvement_by_complexity(domain)

    ax1.plot(gp_avg_rel_improvement_Brute.keys(), gp_avg_rel_improvement_Brute.values(), label="Brute", color="midnightBlue",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_AlteredOneMutationLoops25.keys(), gp_avg_rel_improvement_AlteredOneMutationLoops25.values(), label="Loops 25", color="mediumseagreen",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_AlteredOneMutationLoops50.keys(), gp_avg_rel_improvement_AlteredOneMutationLoops50.values(), label="Loops 50",
             color="mediumpurple",
             marker="o")
    ax1.plot(gp_avg_rel_improvement_AlteredOneMutation.keys(), gp_avg_rel_improvement_AlteredOneMutation.values(), label="Altered One Mutation",
             color="orangered",
             marker="^")
    ax1.plot(gp_avg_rel_improvement_Combination7.keys(), gp_avg_rel_improvement_Combination7.values(), label="Combination 7",
             color="gold",
             marker="o")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Avg. Relative Improvement (%)")
    ax1.set_ylim(ymin=0)
    ax1.legend()
    ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_avg_rel_improvement_Brute = gp_result_parser_robot_Brute.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_AlteredOneMutationLoops25 = gp_result_parser_robot_AlteredOneMutationLoops25.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_AlteredOneMutationLoops50 = gp_result_parser_robot_AlteredOneMutationLoops50.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_AlteredOneMutation = gp_result_parser_robot_AlteredOneMutation.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination7 = gp_result_parser_robot_Combination7.rel_improvement_by_complexity(domain)

    ax2.plot(gp_avg_rel_improvement_Brute.keys(), gp_avg_rel_improvement_Brute.values(), label="Brute", color="midnightBlue",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_AlteredOneMutationLoops25.keys(), gp_avg_rel_improvement_AlteredOneMutationLoops25.values(), label="Loops 25", color="mediumseagreen",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_AlteredOneMutationLoops50.keys(), gp_avg_rel_improvement_AlteredOneMutationLoops50.values(), label="Loops 50",
             color="mediumpurple",
             marker="o")
    ax2.plot(gp_avg_rel_improvement_AlteredOneMutation.keys(), gp_avg_rel_improvement_AlteredOneMutation.values(), label="Altered One Mutation",
             color="orangered",
             marker="^")
    ax2.plot(gp_avg_rel_improvement_Combination7.keys(), gp_avg_rel_improvement_Combination7.values(), label="Combination 7",
             color="gold",
             marker="o")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Avg. Relative Improvement (%)")
    ax2.set_ylim(ymin=0)
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_avg_rel_improvement_Brute = gp_result_parser_string_Brute.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_AlteredOneMutationLoops25 = gp_result_parser_string_AlteredOneMutationLoops25.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_AlteredOneMutationLoops50 = gp_result_parser_string_AlteredOneMutationLoops50.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_AlteredOneMutation = gp_result_parser_string_AlteredOneMutation.rel_improvement_by_complexity(domain)
    gp_avg_rel_improvement_Combination7 = gp_result_parser_string_Combination7.rel_improvement_by_complexity(domain)

    ax3.plot(gp_avg_rel_improvement_Brute.keys(), gp_avg_rel_improvement_Brute.values(), label="Brute", color="midnightBlue",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_AlteredOneMutationLoops25.keys(), gp_avg_rel_improvement_AlteredOneMutationLoops25.values(), label="Loops 25", color="mediumseagreen",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_AlteredOneMutationLoops50.keys(), gp_avg_rel_improvement_AlteredOneMutationLoops50.values(), label="Loops 50",
             color="mediumpurple",
             marker="o")
    ax3.plot(gp_avg_rel_improvement_AlteredOneMutation.keys(), gp_avg_rel_improvement_AlteredOneMutation.values(), label="Altered One Mutation",
             color="orangered",
             marker="^")
    ax3.plot(gp_avg_rel_improvement_Combination7.keys(), gp_avg_rel_improvement_Combination7.values(), label="Combination 7",
             color="gold",
             marker="o")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Avg. Relative Improvement (%)")
    ax3.set_ylim(ymin=0)
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/relative_improvement_loops.svg")
    fig.clf()
    plt.close

def plot_dis_to_correct():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))

# plot_rel_improvement()
plot_complexity_vs_solved_percentage()
plot_error_progression("string", "strings/1-58-1.pl")
plot_complexity_vs_avg_test_cost()
