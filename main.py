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

    # Obtain the domain. Possible domains: "robot", "pixel", "string"
    # If not an argument you can set it here
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = "robot"

    print("domain : " + domain)

    # Obtain the experiment parameters, this holds only for Metropolis-Hastings.
    # If not an argument you can set it here
    if len(sys.argv) > 2:
        params_str = sys.argv[2].replace("'", '"')
    else:
        params = {
          'alpha': 1,
          'type': 'metropolis_hastings',
          'add_token_random': 10,
          'remove_token_random': 20,
          'add_loop_random': 10,
          'add_if_statement_random': 10,
          'start_over': 1,
        }
        params_str = params.__str__().replace("'", '"')

    print("params : " + params_str)

    params = json.loads(params_str)
    print(json.dumps(params, indent=4, sort_keys=True))

    # Possible Search Algorithms: Brute, MCTS, MetropolisHastings, LNS, VanillaGP
    searchAlgos: List[Type[SearchAlgorithm]] = [[MetropolisHasting, "metro"]]


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

