import sqlite3

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# Add seats column
cursor.execute("ALTER TABLE Bookings ADD COLUMN seats TEXT;")

conn.commit()
conn.close()

print("Seats column added to Bookings table successfully!")
