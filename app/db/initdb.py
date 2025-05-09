import sqlite3
import os

base_dir = os.path.dirname(__file__)
schema_path = os.path.join(base_dir, "schema.sql")
db_path = os.path.join(base_dir, "santas.db")

if os.path.exists(db_path):
    print("Database already exists. Skipping initialization.")
else:
    try:
        with open(schema_path, "r") as f:
            schema = f.read()
        conn = sqlite3.connect(db_path)
        conn.executescript(schema)
        conn.commit()
        print("Database initialized.")
    except Exception as e:
        print(f"Database init failed: {e}")
    finally:
        conn.close()