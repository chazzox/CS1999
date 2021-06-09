import json
from app import DATABASE_FILE
import sqlite3
from validate import defaults, database_friendly

connection = sqlite3.connect(DATABASE_FILE)
print('- Opened database successfully in file "{}"'.format(DATABASE_FILE))


connection.execute(
    """CREATE TABLE IF NOT EXISTS buggies (
    id                      INTEGER PRIMARY KEY,
    qty_wheels              INTEGER DEFAULT 4,
    power_type              VARCHAR(20),
    power_units             INTEGER DEFAULT 1,
    aux_power_type          VARCHAR(20),
    aux_power_units         INTEGER DEFAULT 1,
    hamster_booster         INTEGER DEFAULT 0,
    flag_color              VARCHAR(20),
    flag_pattern            VARCHAR(20),
    flag_color_secondary    VARCHAR(20),
    tyres                   VARCHAR(20),
    qty_tyres               INTEGER DEFAULT 4,
    armour                  VARCHAR(20),
    attack                  varchar(20),
    qty_attacks             INTEGER DEFAULT 0,
    fireproof               INTEGER DEFAULT 0,
    insulated               INTEGER DEFAULT 0,
    antibiotic              INTEGER DEFAULT 0,
    banging                 INTEGER DEFAULT 0, 
    algo                    VARCHAR(20),
    total_cost              INTEGER DEFAULT 0
)"""
)


example_db = json.loads(
    """[
  {
    "id": 1, 
    "qty_wheels": 8, 
    "power_type": "bio", 
    "power_units": 6, 
    "aux_power_type": "electric", 
    "aux_power_units": 5, 
    "hamster_booster": 8, 
    "flag_color": "#af0808", 
    "flag_pattern": "hstripe", 
    "flag_color_secondary": "#15760f", 
    "tyres": "steelband", 
    "qty_tyres": 14, 
    "armour": "thicksteel", 
    "attack": "spike", 
    "qty_attacks": 7, 
    "fireproof": 1, 
    "insulated": 1, 
    "antibiotic": 0, 
    "banging": 1, 
    "algo": "titfortat", 
    "total_cost": 832
  }, 
  {
    "id": 3, 
    "qty_wheels": 4, 
    "power_type": "thermo", 
    "power_units": 1, 
    "aux_power_type": "None", 
    "aux_power_units": 0, 
    "hamster_booster": 0, 
    "flag_color": "#191b9a", 
    "flag_pattern": "plain", 
    "flag_color_secondary": "#6f4444", 
    "tyres": "knobbly", 
    "qty_tyres": 4, 
    "armour": "thicksteel", 
    "attack": "None", 
    "qty_attacks": 0, 
    "fireproof": 1, 
    "insulated": 0, 
    "antibiotic": 0, 
    "banging": 1, 
    "algo": "random", 
    "total_cost": 552
  }, 
  {
    "id": 4, 
    "qty_wheels": 4, 
    "power_type": "thermo", 
    "power_units": 1, 
    "aux_power_type": "None", 
    "aux_power_units": 0, 
    "hamster_booster": 0, 
    "flag_color": "#191b9a", 
    "flag_pattern": "dstripe", 
    "flag_color_secondary": "#9d1515", 
    "tyres": "knobbly", 
    "qty_tyres": 4, 
    "armour": "None", 
    "attack": "spike", 
    "qty_attacks": 9, 
    "fireproof": 1, 
    "insulated": 1, 
    "antibiotic": 1, 
    "banging": 1, 
    "algo": "offensive", 
    "total_cost": 707
  }, 
  {
    "id": 5, 
    "qty_wheels": 4, 
    "power_type": "thermo", 
    "power_units": 1, 
    "aux_power_type": "None", 
    "aux_power_units": 0, 
    "hamster_booster": 0, 
    "flag_color": "#191b9a", 
    "flag_pattern": "checker", 
    "flag_color_secondary": "#8e1a1a", 
    "tyres": "knobbly", 
    "qty_tyres": 4, 
    "armour": "None", 
    "attack": "None", 
    "qty_attacks": 0, 
    "fireproof": 1, 
    "insulated": 0, 
    "antibiotic": 0, 
    "banging": 1, 
    "algo": "random", 
    "total_cost": 472
  }, 
  {
    "id": 6, 
    "qty_wheels": 4, 
    "power_type": "thermo", 
    "power_units": 1, 
    "aux_power_type": "None", 
    "aux_power_units": 0, 
    "hamster_booster": 0, 
    "flag_color": "#191b9a", 
    "flag_pattern": "hstripe", 
    "flag_color_secondary": "#8e1a1a", 
    "tyres": "knobbly", 
    "qty_tyres": 4, 
    "armour": "None", 
    "attack": "charge", 
    "qty_attacks": 0, 
    "fireproof": 1, 
    "insulated": 1, 
    "antibiotic": 1, 
    "banging": 1, 
    "algo": "random", 
    "total_cost": 662
  }]""".replace(
        "\n    ", ""
    ).strip()
)


print('- Table "buggies" exists OK')
cursor = connection.cursor()

cursor.execute("SELECT * FROM buggies LIMIT 1")
rows = cursor.fetchall()
if len(rows) == 0:
    for buggy in example_db:
        keys = ", ".join(buggy.keys())
        values = ", ".join(map(lambda a: str(database_friendly(a)), buggy.values()))
        cursor.execute(f"INSERT INTO buggies ({keys}) VALUES ({values})")
        connection.commit()
        print("- Added one 4-wheeled buggy")
else:
    print("- Found a buggy in the database, nice")

print("- OK, your database is ready")


connection.close()
