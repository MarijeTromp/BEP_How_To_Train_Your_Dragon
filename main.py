import sys
from evaluation.experiment_procedure import *
from example_parser.string_parser import StringParser
from search.MCTS.mcts import MCTS
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

if __name__ == "__main__":

    # Settings
    time_limit = 10
    domain = "robot"
    index = int(sys.argv[1])

    algo = [
        # (Brute(time_limit), "Brute"),
        # (RemoveNInsertN(time_limit), "LNS"),
        (RemoveNInsertNVDI(1000, time_limit), "VDNS_1000"),
        (RemoveNInsertNVDI(3000, time_limit), "VDNS_3000"),
        (RemoveNInsertNVDI(5000, time_limit), "VDNS_5000"),
        (RemoveNInsertNVDI(10000, time_limit), "VDNS_10000"),
        (RemoveNInsertNVDI(15000, time_limit), "VDNS_15000"),
        (RemoveNInsertNVDI(30000, time_limit), "VDNS_30000"),
        (RemoveNInsertNVDI(1000, time_limit, Ni_increment=100), "VDNS_1000_Ni100"),
        (RemoveNInsertNVDI(3000, time_limit, Ni_increment=100), "VDNS_3000_Ni100"),
        (RemoveNInsertNVDI(1000, time_limit, init_temp=1, cooling=0.997), "VDNS_1000_Stoch"),
        (RemoveNInsertNVDI(3000, time_limit, init_temp=1, cooling=0.997), "VDNS_3000_Stoch"),
    ][index]

    ranges = {
        "string": [range(1, 101), range(101, 201), range(201, 301), range(301, 328)],
        "robot": [[]],
        "pixel": [[i] for i in range(0, 10)],
    }

    for r in ranges[domain]:
        result = BatchRun(
            # Task domain
            domain=domain,

            # Iterables for files name. Use [] to use all values.
            # This runs all files adhering to format "2-*-[0 -> 10]"
            # Thus, ([], [], []) runs all files for a domain.
            files=([], r, []),

            # Search algorithm to be used
            search_algorithm=algo[0],
            file_name=algo[1] + "-" + time.strftime("%Y%m%d-%H%M%S"),

            # Prints out result when a test case is finished
            print_results=True,

            # Use multi core processing
            multi_core=True,
        ).run()

    # for res in results:
    #     print(res[0], res[1])