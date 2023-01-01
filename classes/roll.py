import d20

def roll(string: str) -> str:
    try:
        roll = d20.roll(string)
        message = str(roll)
        if roll.crit == d20.CritType.CRIT:
            message += f"\n**critical hit!**"
        if roll.crit == d20.CritType.FAIL:
            message += f"\n**critical fail!**"
        return message
    except d20.RollSyntaxError as ex:
        return "a syntactic error occured while rolling your dice."
    except d20.RollValueError as ex:
        return "a bad value was passed to the operator."
    except d20.TooManyRolls as ex:
        return "you roll the dice and it spills all over the floor, you rolled too much dice."
    except Exception as ex:
        return "you roll the dice and it spills into the astral plane never to be seen again."