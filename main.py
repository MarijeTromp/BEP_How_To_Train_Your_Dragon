import itertools
from typing import List
from evaluation.experiment_procedure import *
from example_parser.string_parser import StringParser
from search.MCTS.mcts import MCTS
from search.a_star.a_star import AStar
from search.abstract_search import SearchAlgorithm
from search.gen_prog.vanilla_GP import VanillaGP
from search.gen_prog.vanilla_GP_alternatives.vanilla_GP_reworked import VanillaGPReworked
from search.metropolis_hastings.metropolis import MetropolisHasting
from search.vlns.large_neighborhood_search.algorithms.remove_n_insert_n import RemoveNInsertN
from search.batch_run import BatchRun
from search.vlns.large_neighborhood_search.algorithms.remove_n_insert_n import RemoveNInsertN

if __name__ == "__main__":
    # Possible Search Algorithms: Brute, MCTS, MetropolisHastings, LNS, VanillaGP
    searchAlgos: List[Type[SearchAlgorithm]] = [[MetropolisHasting, "metro"]]

    # Possible domains: "robot", "pixel", "string"
    domains = ["robot"]

    # For gridsearch on algorithm parameters
    param_search_space: dict = {
        "alpha": [1, 1.25, 1.5],
        "add_token": [10, 20, 50],
        "remove_token": [10, 20, 50],
        "add_loop": [10, 20, 50],
        "add_if_statement": [10, 20, 50],
        "start_over": [2, 10, 20]
    }
    param_keys, param_values = zip(*param_search_space.items())
    param_grid_space = [dict(zip(param_keys, v)) for v in itertools.product(*param_values)]

    for domain in domains:
        results = []
        for alg in searchAlgos:
            for params in param_grid_space:
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
