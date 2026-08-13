import sqlite3

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# Add info column
try:
    cursor.execute("ALTER TABLE Movies ADD COLUMN info TEXT DEFAULT ''")
except sqlite3.OperationalError:
    print("Column 'info' already exists")

# Add cast column
try:
    cursor.execute("ALTER TABLE Movies ADD COLUMN cast TEXT DEFAULT ''")
except sqlite3.OperationalError:
    print("Column 'cast' already exists")

conn.commit()
conn.close()
print("Movies table updated successfully!")
