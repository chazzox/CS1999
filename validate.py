from schema import Schema, And, Use, Or


def validate_data(data, schema):
    try:
        validated = Schema(schema).validate(data)
    except Exception as error_msg:
        return (False, error_msg)
    return (True, validated)


def database_friendly(value):
    if isinstance(value, bool):
        return int(value)
    elif isinstance(value, str):
        return f"'{value}'"
    else:
        return value


power_types = [
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
]

flag_patterns = ["plain", "vstripe", "hstripe", "dstripe", "checker", "spot", "None"]

tyre_types = ["knobbly", "slick", "steelband", "reactive", "maglev"]

armour_types = ["None", "wood", "aluminium", "thinsteel", "thicksteel", "titanium"]

attack_types = ["None", "spike", "flame", "charge", "biohazard"]

algo_types = ["steady", "defensive", "offensive", "titfortat", "random", "buggy"]


defaults = {
    "qty_wheels": {
        "name": "Number of wheels",
        "description": [
            "The more wheels, the more traction. But more importantly, quantity of wheels is also a measure of the buggy's size, so an indicator of strength. The chassis of a heavy buggy with too few wheels might break."
            "To put it another way, if you add a lot of mass to your buggy, you'll need to add extra pairs of wheels.",
            "Wheels are free: you pay for the tyres.",
            "Must be even.",
        ],
        "defaults": "4",
        "validation": And(Use(int), lambda n: n >= 4),
        "form": {"type": "num", "min": "4", "max": "", "step": 2},
    },
    "power_type": {
        "name": "Primary motive power",
        "description": [
            "The main source of motive power that moves your buggy forward.",
            "See power table for details.",
        ],
        "defaults": "petrol",
        "validation": Or(*power_types),
        "form": {"type": "select", "options": power_types},
    },
    "power_units": {
        "name": "Primary motive power units",
        "description": [
            "The quantity of primary motive power units. For consumable fuel types this could be quite high; for large expensive types (e.g., nuclear reactors) it may be singular.",
            "Consumable power units are depleted during the race: your buggy gets lighter but you risk running out of fuel.",
            "1 unit of petrol might not get you very far.",
        ],
        "defaults": "1",
        "validation": And(Use(int), lambda n: n >= 1),
        "form": {"type": "num", "min": "1", "max": "", "step": ""},
    },
    "aux_power_type": {
        "name": "Auxiliary motive power",
        "description": [
            "The backup plan for motive power for your buggy. You'll only need this if your primary motive power fails catastrophically, or it runs out of fuel.",
            "You don't need a backup. Nobody needs a backup. Until they do.",
            "See power table for details.",
        ],
        "defaults": "None",
        "validation": Or("None", *power_types),
        "form": {"type": "select", "options": ["None", *power_types]},
    },
    "aux_power_units": {
        "name": "Auxiliary motive power units",
        "description": [
            "The quantity of auxiliary motive power units.",
            "Consumable power units are depleted during the race.",
        ],
        "defaults": "0",
        "validation": And(Use(int), lambda n: n >= 0),
        "form": {"type": "num", "min": "0", "max": "", "step": ""},
    },
    "hamster_booster": {
        "name": "Hamster booster",
        "description": [
            "Steroids for hamsters.",
            "Only effective if you have hamster motive power.",
            "Cost is per booster.",
            "Hamsters can multiboost.",
        ],
        "defaults": "0",
        "validation": And(Use(int), lambda n: n >= 0),
        "form": {"type": "num", "min": "0", "max": "", "step": ""},
    },
    "flag_color": {
        "name": "Flag's colour",
        "description": [
            "Racing buggies must fly a pennant so they can be recognised by the spectators and the race commentators. This is the primary colour of the buggy's pennant."
        ],
        "defaults": "white",
        "validation": str,
        "form": {"type": "color"},
    },
    "flag_pattern": {
        "name": "Flag's pattern",
        "description": [
            "The pattern on the buggy's pennant. Every pattern except plain needs two colours (a primary colour, and a secondary). Stripes may be vertical, horizontal, or diagonal."
        ],
        "defaults": "plain",
        "validation": Or(*flag_patterns),
        "form": {"type": "select", "options": flag_patterns},
    },
    "flag_color_secondary": {
        "name": "Flag's other colour",
        "description": [
            "The other colour of the buggy's pennant, if its pattern has two.",
            "Must be different from flag_color (unless pattern is plain).",
        ],
        "defaults": "black",
        "validation": str,
        "form": {"type": "color"},
    },
    "tyres": {
        "name": "Type of tyres",
        "description": [
            "The type of tyres. Appropriate for different conditions and budgets.",
            "You can only carry one type of tyre (that is, for all your tyres) in any race.",
        ],
        "defaults": "knobbly",
        "validation": Or(*tyre_types),
        "form": {"type": "select", "options": tyre_types},
    },
    "qty_tyres": {
        "name": "Number of tyres",
        "description": [
            "The number of tyres (includes spares).",
            "Must be equal to or greater than the number of wheels",
        ],
        "defaults": 4,
        "validation": And(Use(int), lambda n: n >= 4),
        "form": {"type": "num", "min": "4", "max": "", "step": ""},
    },
    "armour": {
        "name": "Armour",
        "description": [
            "The predominant protection carried by the buggy. A triple-trade-off between safety, encumbrance, and cost.",
            "Only needed if other buggies come equipped for hostilities. Surely nobody brings weapons to a race, right?",
        ],
        "defaults": "None",
        "validation": Or(*armour_types),
        "form": {"type": "select", "options": armour_types},
    },
    "attack": {
        "name": "Offensive capability",
        "description": [
            "Just in case you think you'll win better if you can also spoil other buggies' days, some weapons are available. All can cause operational damage or punctures.",
            "Options are classic spikes, flame throwers, electric lances, or infectious spores.",
            "All except spikes carry a risk of karmic self-injury.",
        ],
        "defaults": "None",
        "validation": Or(*attack_types),
        "form": {"type": "select", "options": attack_types},
    },
    "qty_attacks": {
        "name": "Number of attacks",
        "description": [
            "Every attack is an opportunity to be kind, wasted.",
            "This is the maximum number of attacks that will be attempted during the race.",
        ],
        "defaults": 0,
        "validation": And(Use(int), lambda n: n >= 0),
        "form": {"type": "num", "min": "0", "max": "", "step": ""},
    },
    "fireproof": {
        "name": "Fireproof?",
        "description": ["Is the buggy coated with fire-retardant paint?"],
        "defaults": False,
        "validation": Use(bool),
        "form": {"type": "bool"},
    },
    "insulated": {
        "name": "Insulated?",
        "description": [
            "Is the buggy protected with a rubber mesh protecting itself from electric lance attacks?"
        ],
        "defaults": False,
        "validation": Use(bool),
        "form": {"type": "bool"},
    },
    "antibiotic": {
        "name": "Antibiotic?",
        "description": [
            "Is the buggy equipped with with the latest defences against virulent biohazards and nasty scratches?"
        ],
        "defaults": False,
        "validation": Use(bool),
        "form": {"type": "bool"},
    },
    "banging": {
        "name": "Banging sound system?",
        "description": [
            "Is the buggy wired up with some decent lungs for blasting motivational rock during the more demanding sections of the race?"
        ],
        "defaults": False,
        "validation": Use(bool),
        "form": {"type": "bool"},
    },
    "algo": {
        "name": "Race computer algorithm",
        "description": [
            "Yes, your buggy has a race computer. The primary behavioural characteristic of the program that is loaded affects how it interacts with the other vehicles around it.",
            "Don't start with \"buggy\". Buggy is what happens when your race computer goes wrong: it's not a state you choose.",
            "Must not be buggy.",
        ],
        "defaults": "steady",
        "validation": Or(*algo_types),
        "form": {"type": "select", "options": algo_types},
    },
}

colors = [
    "black",
    "silver",
    "gray",
    "white",
    "maroon",
    "red",
    "purple",
    "fuchsia",
    "green",
    "lime",
    "olive",
    "yellow",
    "navy",
    "blue",
    "teal",
    "aqua",
    "CSS",
    "CSS",
    "antiquewhite",
    "aquamarine",
    "azure",
    "beige",
    "bisque",
    "blanchedalmond",
    "blueviolet",
    "brown",
    "burlywood",
    "cadetblue",
    "chartreuse",
    "chocolate",
    "coral",
    "cornflowerblue",
    "cornsilk",
    "crimson",
    "cya",
    "synonym",
    "darkblue",
    "darkcyan",
    "darkgoldenrod",
    "darkgray",
    "darkgreen",
    "darkgrey",
    "darkkhaki",
    "darkmagenta",
    "darkolivegreen",
    "darkorange",
    "darkorchid",
    "darkred",
    "darksalmon",
    "darkseagreen",
    "darkslateblue",
    "darkslategray",
    "darkslategrey",
    "darkturquoise",
    "darkviolet",
    "deeppink",
    "deepskyblue",
    "dimgray",
    "dimgrey",
    "dodgerblue",
    "firebrick",
    "floralwhite",
    "forestgreen",
    "gainsboro",
    "ghostwhite",
    "gold",
    "goldenrod",
    "greenyellow",
    "grey",
    "honeydew",
    "hotpink",
    "indianred",
    "indigo",
    "ivory",
    "khaki",
    "lavender",
    "lavenderblush",
    "lawngreen",
    "lemonchiffon",
    "lightblue",
    "lightcoral",
    "lightcyan",
    "lightgoldenrodyellow",
    "lightgray",
    "lightgreen",
    "lightgrey",
    "lightpink",
    "lightsalmon",
    "lightseagreen",
    "lightskyblue",
    "lightslategray",
    "lightslategrey",
    "lightsteelblue",
    "lightyellow",
    "limegreen",
    "linen",
    "magent",
    "synonym",
    "mediumaquamarine",
    "mediumblue",
    "mediumorchid",
    "mediumpurple",
    "mediumseagreen",
    "mediumslateblue",
    "mediumspringgreen",
    "mediumturquoise",
    "mediumvioletred",
    "midnightblue",
    "mintcream",
    "mistyrose",
    "moccasin",
    "navajowhite",
    "oldlace",
    "olivedrab",
    "orangered",
    "orchid",
    "palegoldenrod",
    "palegreen",
    "paleturquoise",
    "palevioletred",
    "papayawhip",
    "peachpuff",
    "peru",
    "pink",
    "plum",
    "powderblue",
    "rosybrown",
    "royalblue",
    "saddlebrown",
    "salmon",
    "sandybrown",
    "seagreen",
    "seashell",
    "sienna",
    "skyblue",
    "slateblue",
    "slategray",
    "slategrey",
    "snow",
    "springgreen",
    "steelblue",
    "tan",
    "thistle",
    "tomato",
    "turquoise",
    "violet",
    "wheat",
    "whitesmoke",
    "yellowgreen",
]
