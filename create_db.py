import sqlite3

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

cursor.executescript("""
                     
CREATE TABLE IF NOT EXISTS Movies (
    movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT,
    duration INTEGER
);

CREATE TABLE IF NOT EXISTS Showtimes (
    showtime_id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER,
    time TEXT,
    available_seats INTEGER,
    FOREIGN KEY(movie_id) REFERENCES Movies(movie_id)
);

CREATE TABLE IF NOT EXISTS Bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    showtime_id INTEGER,
    customer_name TEXT,
    num_tickets INTEGER,
    total_price REAL,
    FOREIGN KEY(showtime_id) REFERENCES Showtimes(showtime_id)
);
    CREATE TABLE IF NOT EXISTS Seats (
    seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    showtime_id INTEGER,
    seat_number TEXT,
    is_booked INTEGER DEFAULT 0,
    FOREIGN KEY(showtime_id) REFERENCES Showtimes(showtime_id)
);
""")

# movies = [
#     ("Avengers", "Action", 180),
#     ("KGF", "Action", 170),
#     ("Frozen", "Animation", 120)
# ]

cursor.execute(
    "INSERT INTO Movies (title, genre, duration) VALUES (?, ?, ?)"
    
)

shows = [
    (1, '2026-02-05 10:00 AM', 100),
    (2, '2026-02-03 08:30 PM', 50),
    (3, '2026-02-05 03:15 AM', 60)
]

cursor.executemany(
    "INSERT INTO Showtimes (movie_id, time, available_seats) VALUES (?, ?, ?)",
    shows
)

conn.commit()
conn.close()

print("Database Created Successfully!")
