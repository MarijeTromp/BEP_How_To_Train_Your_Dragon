import itertools
from typing import List
import sys
import json
#
from evaluation.experiment_procedure import *
from search.abstract_search import SearchAlgorithm
from search.batch_run import BatchRun
from search.metropolis_hastings.metropolis import MetropolisHasting

if __name__ == "__main__":

    # Obtain the experiment parameters
    params_str = sys.argv[1].replace("'", '"')
    params = json.loads(params_str)
    print(json.dumps(params, indent=4, sort_keys=True))

    # Possible Search Algorithms: Brute, MCTS, MetropolisHastings, LNS, VanillaGP
    searchAlgos: List[Type[SearchAlgorithm]] = [[MetropolisHasting, "metro"]]

    # Possible domains: "robot", "pixel", "string"
    domains = ["robot"]

    for domain in domains:
        results = []
        for alg in searchAlgos:
            result = BatchRun(
                # Task domain
                domain=domain,

                # Iterables for files name. Use [] to use all values.
                # This runs all files adhering to format "2-*-[0 -> 10]"
                # Thus, ([], [], []) runs all files for a domain.
                files=([], [], []),

                # Search algorithm to be used
                search_algorithm=alg[0](60, params),

                # Prints out result when a test case is finished
                print_results=True,

                # Use multi core processing
                multi_core=True,

                # Use file_name= to append to a file whenever a run got terminated
                # Comment out argument to create new file.
                # file_name="VLNS-20211213-162128.txt"
            ).run()

        for res in results:
            print(res[0], res[1])





    #
    # # For gridsearch on algorithm parameters
    # param_search_space: dict = {
    #     "alpha": [0.25, 0.5, 0.75, 1, 1.25, 1.5],
    #     "add_token_end": [10, 20, 30, 40, 50],
    #     "remove_token_end": [10, 20, 30, 40, 50],
    #     "add_loop_end": [10, 20, 30, 40, 50],
    #     "add_if_statement_end": [10, 20, 30, 40, 50],
    #     "start_over": [1, 2, 3, 4, 5]
    # }
    #
    # # param_search_space: dict = {
    # #     "alpha": [0.25, 0.5, 0.75, 1, 1.25, 1.5],
    # #     "add_token_end": [10],
    # #     "remove_token_end": [10],
    # #     "add_loop_end": [10],
    # #     "add_if_statement_end": [10],
    # #     "start_over": [1]
    # # }
    #
    #
    #
    # param_keys, param_values = zip(*param_search_space.items())
    # param_grid_space = [dict(zip(param_keys, v)) for v in itertools.product(*param_values)]
    #
    # for domain in domains:
    #     results = []
    #     for alg in searchAlgos:
    #         for params in param_grid_space:
    #             result = BatchRun(
    #                 # Task domain
    #                 domain=domain,
    #
    #                 # Iterables for files name. Use [] to use all values.
    #                 # This runs all files adhering to format "2-*-[0 -> 10]"
    #                 # Thus, ([], [], []) runs all files for a domain.
    #                 files=([], [], []),
    #
    #                 # Search algorithm to be used
    #                 search_algorithm=alg[0](60, params),
    #
    #                 # Prints out result when a test case is finished
    #                 print_results=True,
    #
    #                 # Use multi core processing
    #                 multi_core=True,
    #
    #                 # Use file_name= to append to a file whenever a run got terminated
    #                 # Comment out argument to create new file.
    #                 # file_name="VLNS-20211213-162128.txt"
    #             ).run()
    #
    #     for res in results:
    #         print(res[0], res[1])
