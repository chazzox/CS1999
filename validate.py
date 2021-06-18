from schema import Schema
from constants import ATTACK_DICT, POWER_DICT, TYRE_DICT, ARMOUR_DICT, DEFAULTS


def calc_price(data):
    cost = 0
    # power
    cost += POWER_DICT[data["power_type"]] * data["power_units"]
    cost += ({**POWER_DICT, "None": 0}[data["aux_power_type"]]) * data["aux_power_units"]
    # tyre
    cost += data["qty_tyres"] * TYRE_DICT[data["tyres"]]
    # armour
    cost += ARMOUR_DICT[data["armour"]] * (1 + 0.1 * (data["qty_tyres"] - 4))
    # attack
    cost += data["qty_attacks"] * ATTACK_DICT[data["attack"]]
    # hamster boosters
    cost += 5 * data["hamster_booster"]
    # everything else
    for i in DEFAULTS.keys():
        cost += DEFAULTS[i]["cost"] if data[i] else 0

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
    # GAME RULES
    # qty_tyres >= qty_wheels
    if not (validated["qty_tyres"] >= validated["qty_wheels"]):
        return (False, "Quantity of tyres needs to be greater or equal to Quantity of wheels")
    # 1x non-consumable reactor unit
    # TODO: implement setting 1x unit of fuel upon selection of reactor on client side
    if (
        validated["power_type"] in ["fusion", "thermo", "solar", "wind"]
        and validated["power_units"] != 1
    ) or (
        validated["aux_power_type"] in ["fusion", "thermo", "solar", "wind"]
        and validated["aux_power_units"] != 1
    ):
        return (False, "For non-consumable reactor types you can only have 1 unit of power")

    return (True, validated)


def database_friendly(value):
    if isinstance(value, bool):
        return int(value)
    elif isinstance(value, str):
        return f"'{value}'"
    else:
        return value
