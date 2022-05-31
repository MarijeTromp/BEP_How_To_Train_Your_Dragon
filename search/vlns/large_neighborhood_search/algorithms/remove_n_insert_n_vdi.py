
from search.vlns.large_neighborhood_search.accept.deterministic_accept import DeterministicAccept
from search.vlns.large_neighborhood_search.accept.stochastic_accept import StochasticAccept
from search.vlns.large_neighborhood_search.destroy.remove_n_destroy import ExtractNDestroy
from search.vlns.large_neighborhood_search.invent.static_invent import StaticInvent
from search.vlns.large_neighborhood_search.invent.variable_depth_invent import VariableDepthInvent
from search.vlns.large_neighborhood_search.large_neighborhood_search import LNS
from search.vlns.large_neighborhood_search.repair.insert_n_repair import InsertNRepair


class RemoveNInsertNVDI(LNS):

    def __init__(self, inc_depth_after: int, time_limit=10, Ni_increment=0, init_temp = 0, cooling: float = 0):
        super().__init__(
            time_limit=time_limit,

            accept = StochasticAccept(initial_temperature=init_temp, cooling_factor=cooling) if ((init_temp != 0) & (cooling != float(0))) else DeterministicAccept(),
            # accept=DeterministicAccept(),

            destroy=ExtractNDestroy(initial_max_n=3, max_max_n=3),

            repair=InsertNRepair(initial_max_n=3, max_max_n=3, w_trans=1, w_loop=1, w_if=0),

            #invent=StaticInvent(),
            invent=VariableDepthInvent(depths=[(1, 1), (2, 1), (2, 2)]),

            increase_depth_after=inc_depth_after,

            Ni_increment=Ni_increment,

            debug=False,
        )
