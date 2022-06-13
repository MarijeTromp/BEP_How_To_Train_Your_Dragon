import sys
from evaluation.experiment_procedure import *
from example_parser.string_parser import StringParser
# from search.MCTS.mcts import MCTS
from search.a_star.a_star import AStar
from search.abstract_search import SearchAlgorithm
from search.gen_prog.vanilla_GP import VanillaGP
from search.metropolis_hastings.metropolis import MetropolisHasting
from search.vlns.large_neighborhood_search.algorithms.flute_brute import FluteBrute
from search.vlns.large_neighborhood_search.algorithms.flute_brute_vdi import FluteBruteVDI
from search.vlns.large_neighborhood_search.algorithms.remove_n_insert_n import RemoveNInsertN
from search.batch_run import BatchRun
from search.vlns.large_neighborhood_search.algorithms.remove_n_insert_n import RemoveNInsertN
from search.vlns.large_neighborhood_search.algorithms.remove_n_insert_n_vdi import RemoveNInsertNVDI
from search.vlns.large_neighborhood_search.accept.deterministic_accept import DeterministicAccept
from search.vlns.large_neighborhood_search.accept.stochastic_accept import StochasticAccept

if __name__ == "__main__":

    # Settings
    time_limit = 10
    domain = "robot"
    index = int(sys.argv[1])

    algo = [
        # initial_max_n=3, max_max_n=3, w_trans=1, w_loop=1, w_if=0, strategy= random
        # (Brute(time_limit), "Brute"),
        # (RemoveNInsertN(time_limit), "LNS"),
        (RemoveNInsertNVDI(1000, time_limit, prune=True), "VDNS_1000_prune"),
        # (RemoveNInsertNVDI(1000, time_limit, strategy="random"), "VDNS_1000_ran"),
        # (RemoveNInsertNVDI(1000, time_limit, strategy="increasing"), "VDNS_1000_inc"),
        # (RemoveNInsertNVDI(1000, time_limit, strategy="decreasing"), "VDNS_1000_dec"),
        # (RemoveNInsertNVDI(10000, time_limit, strategy="random"), "VDNS_10000_ran"),
        # (RemoveNInsertNVDI(10000, time_limit, strategy="increasing"), "VDNS_10000_inc"),
        # (RemoveNInsertNVDI(10000, time_limit, strategy="decreasing"), "VDNS_10000_dec"),
        # (RemoveNInsertNVDI(1000, time_limit), "VDNS_1000"),
        # (RemoveNInsertNVDI(3000, time_limit), "VDNS_3000"),
        # (RemoveNInsertNVDI(1000, time_limit, Ni_increment=100), "VDNS_1000_Ni100"),,
        # (RemoveNInsertNVDI(3000, time_limit, best_improvement=10), "VDNS_3000_BestImp"),
        # (RemoveNInsertNVDI(10000, time_limit, accept=StochasticAccept(float(0.1), float(0.997))), "VDNS_10000_Stoch"),
    ]

    ranges = {
        "string": [range(1, 101), range(101, 201), range(201, 301), range(301, 328)],
        "robot": [[]],
        "pixel": [[]], #[[i] for i in range(0, 10)],
    }
    result = []

    for alg in algo:
        for r in ranges[domain]:

            result = BatchRun(
                # Task domain
                domain=domain,

                # Iterables for files name. Use [] to use all values.
                # This runs all files adhering to format "2-*-[0 -> 10]"
                # Thus, ([], [], []) runs all files for a domain.
                files=([], r, []),

                # Search algorithm to be used
                search_algorithm=alg[0],
                file_name=alg[1] + "-" + time.strftime("%Y%m%d-%H%M%S"),

                # Prints out result when a test case is finished
                print_results=True,

                # Use multi core processing
                multi_core=True,
            ).run()

    # for res in results:
    #     print(res[0], res[1])