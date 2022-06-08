from common.environment import Environment

class Equivalence_Classes:
    def __init__(self):
        self.classes: dict = {} # dict: {keys: Input World, values: (dict: { keys: cost, values: counter})}

    def get_count(self, input_world: Environment, cost: int) -> int:
        input_stats: dict = self.classes.get(input_world)

        if input_stats is None:
            self.classes[input_world] = {cost: 1}
            return 1

        output_counter: int = input_stats.get(cost)

        if output_counter is None:
            output_counter = 1
        else:
            output_counter = output_counter + 1

        self.classes[input_world][cost] = output_counter
        return output_counter
