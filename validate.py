from jsonschema import validate
from schema import Schema, And, Use, Or, Optional

schema = {
    "type": "object",
    "properties": {
        "id": {"title": "Id of buggy", "type": "integer"},
        "qty_wheels": {
            "title": "Number of wheels",
            "type": "integer",
            "minimum": 4,
            "multipleOf": 2,
        },
        "power_type": {
            "title": "Primary motive power",
            "enum": [
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
            ],
        },
        "power_units": {
            "title": "Primary motive power units",
            "type": "integer",
            "multipleOf": 2,
        },
        "aux_power_type": {
            "title": "Auxiliary motive power",
            "enum": [
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
            ],
        },
        "aux_power_units": {"title": "Auxiliary motive power units", "type": "integer"},
        "hamster_booster": {"title": "Hamster booster", "type": "integer"},
        "flag_pattern": {
            "title": "Flag's pattern",
            "enum": ["plain", "vstripe", "hstripe", "dstripe", "checker", "spot"],
        },
        "flag_color": {"title": "Flag's colour", "type": "string"},
        "flag_color_secondary": {"title": "Flag's pattern", "type": "string"},
        "tyres": {
            "title": "Type of tyres",
            "enum": ["knobbly", "slick", "steelband", "reactive", "maglev"],
        },
        "qty_tyres": {"title": "Number of tyres", "type": "integer", "minimum": 4},
        "armour": {
            "title": "Armour",
            "enum": ["wood", "aluminium", "thinsteel", "thicksteel", "titanium"],
        },
        "attack": {
            "title": "Offensive capability",
            "enum": ["spike", "flame", "charge", "biohazard"],
        },
        "qty_attacks": {"title": "Number of attacks", "type": "integer"},
        "fireproof": {"title": "Fireproof?", "type": "boolean"},
        "insulated": {"title": "Insulated?", "type": "boolean"},
        "antibiotic": {"title": "Antibiotic?", "type": "boolean"},
        "banging": {"title": "Banging sound system?", "type": "boolean"},
        "algo": {
            "title": "Race computer algorithm",
            "enum": [
                "defensive",
                "steady",
                "offensive",
                "titfortat",
                "random",
                "buggy",
            ],
        },
    },
    "required": [],
    "additionalProperties": False,
    "$id": "buggy",
}


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

schema2 = Schema(
    [
        {
            "id": Use(int),
            "qty_wheels": And(Use(int), lambda n: n >= 4),
            "power_type": power_types,
            "power_units": And(Use(int), lambda n: n >= 1),
            "aux_power_type": power_types,
            "aux_power_units": And(Use(int), lambda n: n >= 0),
            "hamster_booster": Use(int),
            "flag_color": str,
            "flag_pattern": Or(
                "plain", "vstripe", "hstripe", "dstripe", "checker", "spot"
            ),
            "flag_color_secondary": str,
            "tyres": Or("knobbly", "slick", "steelband", "reactive", "maglev"),
            "qty_tyres": And(Use(int), lambda n: n >= 4),
            "armour": Or(
                "none", "wood", "aluminium", "thinsteel", "thicksteel", "titanium"
            ),
            "attack": Or("none", "spike", "flame", "charge", "biohazard"),
            "qty_attacks": And(Use(int), lambda n: n >= 0),
            "fireproof": bool,
            "insulated": bool,
            "antibiotic": bool,
            "banging": bool,
            "algo": Or(
                "defensive", "steady", "offensive", "titfortat", "random", "buggy"
            ),
        }
    ]
)

test = schema2.validate([])
print(test)


def validate_data(data):
    try:
        validate(instance=data, schema=schema)
    except Exception as error_msg:
        return (False, error_msg)
    return (True, "")
