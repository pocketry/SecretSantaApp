import sqlite3
import json

with open("./schema.sql", "r") as f:
    schema = f.read()

try:
    conn = sqlite3.connect("santas.db")
    conn.executescript(schema)
    conn.commit()
except Exception as e:
    print(f"Database init failed: {e}")


# with open ("./testSantas.json", "r") as f:
#     testSantas = json.load(f)

 