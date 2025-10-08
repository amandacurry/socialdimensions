import sqlite3
import pandas as pd

DB_NAME = "annotations.db"

# Connect to the database
conn = sqlite3.connect(DB_NAME)

# Example: load the entire annotations table
annotations = pd.read_sql("SELECT * FROM annotations", conn)
print(annotations.head())  # show the first 5 rows

# Example: load stimuli table
stimuli = pd.read_sql("SELECT * FROM stimuli", conn)
print(stimuli.head())

# Example: load demographics table
demographics = pd.read_sql("SELECT * FROM demographics", conn)
print(demographics.head())

conn.close()