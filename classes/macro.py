"""
This class is used to create, parse, and serialize macros.
"""
from typing import List
from d20 import roll, RollResult


def do_macro(
        macro: str,
        args: List[str]  # String instead of number so that we can support passing dice rolls.
        ) -> RollResult:
    result = macro
    for k, arg in enumerate(map(lambda x: roll(x), args)):
        result = result.replace(f"${k}", str(arg.total))
    return roll(result)
