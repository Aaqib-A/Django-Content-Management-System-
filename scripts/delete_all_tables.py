# NOTE: To run this script use the following command
# python scripts/delete_all_tables.py

import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get a list of all tables (excluding sqlite_sequence)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence';")
tables = cursor.fetchall()

# Drop each table
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")

# Commit the changes and close the connection
conn.commit()
conn.close()
