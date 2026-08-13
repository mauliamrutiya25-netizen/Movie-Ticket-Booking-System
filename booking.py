from app import get_connection

def get_movies():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Movies")   #get all the rows from the movie
    data = cur.fetchall()
    conn.close()
    return data

def get_showtimes(movie_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Showtimes WHERE movie_id=?", (movie_id,))   #gets all showtime for specific movie, (movie_id,) passes the value safely in place of (?).
    data = cur.fetchall()
    conn.close()
    return data

def book_ticket(showtime_id, name, seats):
    conn = get_connection()
    cur = conn.cursor()
    # 👉 In short: conn.cursor() gives you the object that actually talks to the database using SQL.

    # Check if seats are available
    placeholders = ','.join(['?']*len(seats))   #checks seats availability
    cur.execute(f"SELECT seat_number FROM Seats WHERE showtime_id=? AND seat_number IN ({placeholders}) AND is_booked=0", (showtime_id, *seats))   
    available = cur.fetchall()
    if len(available) != len(seats):   #this checks available_seats != to required seats then booking fails
        conn.close()
        return False
    
    # Calculate price
    cur.execute("SELECT price FROM Showtimes WHERE showtime_id=?", (showtime_id,))
    price = cur.fetchone()[0]
    total_price = price * len(seats)
    
    # Insert booking
    cur.execute(
        "INSERT INTO Bookings (showtime_id, customer_name, seats, total_price) VALUES (?, ?, ?, ?)",
        (showtime_id, name, ",".join(seats), total_price)
    )
    
    # Mark seats as booked
    cur.execute(f"UPDATE Seats SET is_booked=1 WHERE showtime_id=? AND seat_number IN ({placeholders})", (showtime_id, *seats))
    
    # Update available_seats in Showtimes
    cur.execute("UPDATE Showtimes SET available_seats = available_seats - ? WHERE showtime_id=?", (len(seats), showtime_id))
    
    conn.commit()
    conn.close()
    
    return total_price


def get_seats(showtime_id):
    """Return all seats for a showtime and whether they are booked."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT seat_number, is_booked FROM Seats WHERE showtime_id=?", (showtime_id,))   #seats no. stored as s1,s2 and Saves 
    seats = cur.fetchall()
    conn.close()
    return seats

def initialize_seats(showtime_id, total_seats):
    """Create seats for a new showtime if not already created."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Seats WHERE showtime_id=?", (showtime_id,))
    count = cur.fetchone()[0]
    if count == 0:
        seats = [(showtime_id, f"S{i+1}") for i in range(total_seats)]
        cur.executemany("INSERT INTO Seats (showtime_id, seat_number) VALUES (?, ?)", seats)
        conn.commit()
    conn.close()

