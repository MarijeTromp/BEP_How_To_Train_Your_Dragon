from common_environment.abstract_tokens import *


class Program:
    """Wrapper class for a list of Tokens, a program."""

    def __init__(self, tokens: List[EnvToken], recurse_limit: int = 300):
        """Creates a new program given a sequence of Tokens."""
        self.sequence = tokens
        self.recursive_call_limit = recurse_limit
    
    def __gt__(self, other):
        if(len(self.sequence)>len(other.sequence)):
            return True
        else:
            return False

    def interp(self, env: Environment, top_level_program=True) -> Environment:
        """Interprets this program on a given Environment, returns the resulting Environment."""

        # Setup for recursive calls
        if top_level_program:
            env.program = self

        for t in self.sequence:
            env = t.apply(env)

        return env

    def number_of_tokens(self) -> int:
        return sum([t.number_of_tokens() for t in self.sequence])

    def __str__(self):
        return "Program([%s])" % ", ".join([str(t) for t in self.sequence])

    def to_formatted_string(self):
        return "Program:\n\t%s" % "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.sequence])

    # def interp_cast(self, env: Environment):
    #   return cast(env, self.interp(env))
