from enum import Enum
from typing import Optional
import d20


class RollResultType(Enum):
    SUCCESS = 0
    FAIL_UNKNOWN = 1
    FAIL_SYNTAX_ERROR = 2
    FAIL_VALUE_ERROR = 3
    FAIL_TOO_MANY_ROLLS = 4


class RollResult():
    message: str
    exception: Optional[Exception]
    result_type: RollResultType

    @property
    def is_ok(self):
        return self.result_type == RollResultType.SUCCESS

    def __init__(self, message: str, result_type: RollResultType, exception: Optional[Exception]):
        self.message = message
        self.result_type = result_type
        self.exception = exception


def roll_with_text(string: str, times: int = 1) -> RollResult:
    result = RollResult("You shouldn't be able to read this", 0, None)
    roll_string: list[str] = string.split(",")

    try:
        roll_results = []
        for _ in range(times):
            for roll in roll_string:
                roll_result = d20.roll(roll.strip())
                message = str(roll_result)
                if roll_result.crit != d20.CritType.NONE:
                    message = f"**{message}**"
                roll_results.append(message)

        result.message = "\n".join(roll_results)
        result.result_type = RollResultType.SUCCESS

    except d20.RollSyntaxError as ex:
        result.exception = ex
        result.message = \
            "a syntactic error occured while rolling your dice."
        result.result_type = RollResultType.FAIL_SYNTAX_ERROR
    except d20.RollValueError as ex:
        result.exception = ex
        result.message = \
            "a bad value was passed to the operator."
        result.result_type = RollResultType.FAIL_VALUE_ERROR
    except d20.TooManyRolls as ex:
        result.exception = ex
        result.message = \
            "you roll the dice and it spills all over the floor, you rolled too much dice."
        result.result_type = RollResultType.FAIL_TOO_MANY_ROLLS
    except Exception as ex:
        result.message = \
            "you roll the dice and it spills into the astral plane never to be seen again."
        result.result_type = RollResultType.FAIL_UNKNOWN
        result.exception = ex

    return result
