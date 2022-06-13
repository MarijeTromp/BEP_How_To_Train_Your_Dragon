from common.environment import Environment

class Equivalence_Classes:
    def __init__(self):
        self.classes: dict = {} # dict: {keys: Input World, values: (dict: { keys: cost, values: counter})}

    def get_count(self, input_world: Environment, output_world: Environment, cost: int) -> int:
        key = (input_world, output_world)
        input_stats: dict = self.classes.get(key)

        if input_stats is None:
            self.classes[key] = {cost: 1}
            return 1

        output_counter: int = input_stats.get(cost)

        if output_counter is None:
            output_counter = 1
        else:
            output_counter = output_counter + 1

        self.classes[key][cost] = output_counter
        return output_counter
