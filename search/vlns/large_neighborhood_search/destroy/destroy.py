from common.prorgam import Program, EnvToken


class Destroy:
    """Interface for destroy methods."""

    def destroy(self, program: Program, i: int = 0, Ni: int = 0) -> list[list[EnvToken]]:
        """Destructs a given program. Returns a list of token sequences."""

        raise NotImplementedError()

    def reset(self):
        pass

    def increment_search_depth(self):
        pass