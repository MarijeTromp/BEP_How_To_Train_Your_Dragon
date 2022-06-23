import json

f = open('../../../../results/string/AlteredOneMutation.txt')

data = [json.loads(line) for line in f]

test_cost = 0
train_cost = 0
time_out = 0
iterations = 0
incorrect_with_if = 0
incorrect_with_loop = 0
total_incorrect = 0

total_correct = 0
correct_programs_with_loop = 0
correct_programs_with_if = 0

total = 0
total_if = 0
total_loop = 0

loops_no_timeout = 0
loops_timeout = 0

for i in data:
    total += 1
    if "If" in i["program"]:
        total_if += 1
    if "Loop" in i["program"]:
        total_loop += 1
    if i["test_cost"] == 0:
        total_correct += 1
        if "If" in i["program"]:
            correct_programs_with_if += 1
        if "Loop" in i["program"]:
            correct_programs_with_loop += 1
    else:
        total_incorrect += 1
        if "If" in i["program"]:
            incorrect_with_if += 1
        if "Loop" in i["program"]:
            incorrect_with_loop += 1
        if i["test_cost"] == float("inf") and i["train_cost"] == 0:
            if "Loop" in i["program"]:
                loops_no_timeout += 1
            test_cost += 1
        if i["execution_time"] >= 60:
            time_out += 1
            if "Loop" in i["program"]:
                loops_timeout += 1
        if i["number_of_iterations"] >= 200:
            iterations += 1
            if "Loop" in i["program"]:
                loops_timeout += 1
        if (not i["test_cost"] == float("inf")) and (not i["execution_time"] >= 60) and (not i["number_of_iterations"] >= 200) and i["train_cost"] == 0:
            train_cost += 1
            if "Loop" in i["program"]:
                loops_no_timeout += 1

if total_incorrect == 0:
    print("\nCorrect programs with if: " + str(correct_programs_with_if / total_correct * 100) + "\nCorrect programs with loop: " + str(
        correct_programs_with_loop / total_correct * 100))
else:
    print("\n" + "Test cost: " + str(test_cost / total_incorrect * 100) + "\nTrain cost: " + str(train_cost / total_incorrect * 100) + "\nTime-out: " + str(time_out / total_incorrect * 100) + "\nIterations: " + str(iterations / total_incorrect * 100) + "\nTotal: " + str(total_incorrect))
    print("\nCorrect programs with if: " + str(correct_programs_with_if / total_correct * 100) + "\nCorrect programs with loop: " + str(correct_programs_with_loop / total_correct * 100))
    print("\nIncorrect programs with if: " + str(incorrect_with_if / total_incorrect * 100) + "\nIncorrect programs with loop: " + str(incorrect_with_loop / total_incorrect * 100))
    print("\nPrograms with if: " + str(total_if / total * 100) + "\nPrograms with loop: " + str(total_loop / total * 100))
    print("\nLoops timeout and iterations: " + str(loops_timeout / total_incorrect * 100) + "\nLoops inf and train: " + str(loops_no_timeout / total_incorrect * 100))
    print("\nPercentage of programs that contains a loop and is correct: " + str(correct_programs_with_loop / total * 100) + "\nPercentage of programs that contains a loop and is incorrect: " + str(incorrect_with_loop / total * 100))
    print("\nPercentage of programs that contains a loop and has a timeout or max iterations " + str(loops_timeout / total * 100) + "\nPercentage of programs that contains a loop and has train cost of 0: " + str(loops_no_timeout / total * 100))