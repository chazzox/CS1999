from jsonschema import validate
from schema import Schema, And, Use, Or, Optional

power_types = Schema(
    Or(
        "petrol",
        "fusion",
        "steam",
        "bio",
        "electric",
        "rocket",
        "hamster",
        "thermo",
        "solar",
        "wind",
    )
)

schema = {
    "id": Use(int),
    "qty_wheels": And(Use(int), lambda n: n >= 4),
    "power_type": power_types,
    "power_units": And(Use(int), lambda n: n >= 1),
    "aux_power_type": Or(None, power_types),
    "aux_power_units": And(Use(int), lambda n: n >= 0),
    "hamster_booster": Use(int),
    "flag_color": str,
    "flag_pattern": Or(
        None, "plain", "vstripe", "hstripe", "dstripe", "checker", "spot"
    ),
    "flag_color_secondary": str,
    "tyres": Or("knobbly", "slick", "steelband", "reactive", "maglev"),
    "qty_tyres": And(Use(int), lambda n: n >= 4),
    "armour": Or(None, "wood", "aluminium", "thinsteel", "thicksteel", "titanium"),
    "attack": Or(None, "spike", "flame", "charge", "biohazard"),
    "qty_attacks": And(Use(int), lambda n: n >= 0),
    "fireproof": bool,
    "insulated": bool,
    "antibiotic": bool,
    "banging": bool,
    "algo": Or("defensive", "steady", "offensive", "titfortat", "random", "buggy"),
}


def validate_data(data):
    try:
        validated = Schema(schema).validate(data)
    except Exception as error_msg:
        print(error_msg)
        return (False, error_msg)
    print(validated)
    return (True, validated)


defaults = {
    "id": "3",
    "qty_wheels": "4",
    "power_type": "petrol",
    "power_units": "1",
    "aux_power_type": None,
    "aux_power_units": "0",
    "hamster_booster": "0",
    "flag_color": "white",
    "flag_pattern": "plain",
    "flag_color_secondary": "black",
    "tyres": "knobbly",
    "qty_tyres": 4,
    "armour": None,
    "attack": None,
    "qty_attacks": 0,
    "fireproof": False,
    "insulated": False,
    "antibiotic": False,
    "banging": False,
    "algo": "steady",
}

validate_data(defaults)
