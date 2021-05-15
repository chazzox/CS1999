from jsonschema import validate

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


def validate_data(data):
    try:
        validate(instance=data, schema=schema)
    except Exception as error_msg:
        return (False, error_msg)
    return (True, "")
