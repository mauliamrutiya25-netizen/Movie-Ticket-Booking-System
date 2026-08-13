import sqlite3

# Connect to your existing database
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# Add the price column with default 250
cursor.execute("ALTER TABLE Showtimes ADD COLUMN price REAL DEFAULT 250;")

conn.commit()
conn.close()

print("Price  column added successfully!")
