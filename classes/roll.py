import d20


def roll_with_text(string: str) -> str:
    roll_string = string.split(",")
    result = []

    try:
        for roll in roll_string:
            roll_result = d20.roll(roll)
            message = str(roll_result)
            if roll_result.crit != d20.CritType.NONE:
                message = f"**{message}**"
            result.append(message)

        return "\n".join(result)

    except d20.RollSyntaxError:  # as ex:
        return "a syntactic error occured while rolling your dice."
    except d20.RollValueError:  # as ex:
        return "a bad value was passed to the operator."
    except d20.TooManyRolls:  # as ex:
        return "you roll the dice and it spills all over the floor, you rolled too much dice."
    except Exception as ex:
        print(ex)
        return "you roll the dice and it spills into the astral plane never to be seen again."
