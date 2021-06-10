from schema import Schema
from constants import ATTACK_DICT, POWER_DICT, TYRE_DICT, ARMOUR_DICT, DEFAULTS


def calc_price(data):
    cost = 0
    # power
    cost += POWER_DICT[data["power_type"]]
    cost += (
        POWER_DICT[data["aux_power_type"]]
        if data["aux_power_type"] in POWER_DICT
        else 0
    )

    # tyre
    cost += data["qty_tyres"] * TYRE_DICT[data["tyres"]]
    # armour
    cost += ARMOUR_DICT[data["armour"]] * (0.1 * data["qty_tyres"])
    # attack
    cost += data["qty_attacks"] * ATTACK_DICT[data["attack"]]
    # everything else
    for i in DEFAULTS.keys():
        cost += DEFAULTS[i]["cost"] if data[i] else 0
    # others
    return cost


validation_dict = dict(map(lambda a: [a[0], a[1]["validation"]], DEFAULTS.items()))


def make_dict(func):
    def wrapper(num):
        return func(dict(num))

    return wrapper


@make_dict
def validate_data(data):
    try:
        validated = Schema(validation_dict).validate(data)
    except Exception as error_msg:
        return (False, error_msg)
    # TODO: GAME RULES
    # TODO: Add better error message
    return (True, validated)


def database_friendly(value):
    if isinstance(value, bool):
        return int(value)
    elif isinstance(value, str):
        return f"'{value}'"
    else:
        return value
