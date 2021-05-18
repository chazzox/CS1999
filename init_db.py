from app import DATABASE_FILE
import sqlite3

connection = sqlite3.connect(DATABASE_FILE)
print('- Opened database successfully in file "{}"'.format(DATABASE_FILE))

# using Python's triple-quote for multi-line strings:
connection.execute(
    """
  	CREATE TABLE IF NOT EXISTS buggies (
    id                    	INTEGER PRIMARY KEY,
    qty_wheels            	INTEGER DEFAULT 4,
	power_type				VARCHAR(20),
	power_units				INTEGER DEFAULT 1,
	aux_power_type			VARCHAR(20),
	aux_power_units			INTEGER DEFAULT 1,
	hamster_booster 		INTEGER DEFAULT 0,
    flag_color            	VARCHAR(20),
    flag_pattern          	VARCHAR(20),
    flag_color_secondary  	VARCHAR(20),
	tyres					VARCHAR(20),
	qty_tyres 				INTEGER DEFAULT 4,
	armour					VARCHAR(20),
	attack					varchar(20),
	qty_attacks				INTEGER DEFAULT 0,
	algo					VARCHAR(20)
  )
"""
)

print('- Table "buggies" exists OK')
cursor = connection.cursor()

cursor.execute("SELECT * FROM buggies LIMIT 1")
rows = cursor.fetchall()
if len(rows) == 0:
    cursor.execute("INSERT INTO buggies (qty_wheels) VALUES (4)")
    connection.commit()
    print("- Added one 4-wheeled buggy")
else:
    print("- Found a buggy in the database, nice")

print("- OK, your database is ready")

connection.close()
