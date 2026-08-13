# 🎟️ Streamlit Movie Ticket Booking System

A modern, lightweight, and interactive **Movie Ticket Booking System** built using **Streamlit** for the user interface and **SQLite** for database management. The application features custom dark-themed styling, interactive seat selection, a mock payment portal, and a comprehensive admin panel for movie and theater management.

---

## 🚀 Features

### 👤 User Panel

- **Interactive Movie Details:** View genre, duration, synopsis, and cast lists.
- **Showtime Selection:** Dynamically browse available showtimes, prices, and seats remaining.
- **Interactive Seat Grid:** A visual grid-based seat selector with 10 seats per row. Seats are marked as booked or available and update in real-time.
- **Mock Payment Portal:**
  - Supports multiple payment channels: **UPI, Credit/Debit Card, and Net Banking**.
  - Built-in input validation for payment details.
  - Processes bookings and displays a detailed transactional receipt.

### 📊 Admin Panel

- **Live Dashboard Metrics:** Displays aggregate analytics including Total Bookings and Total Revenue.
- **Booking Reports:** Search, filter, and view detailed booking records grouped by movie and showtime.
- **Movie Inventory Management:** Easily add or delete movies from the database.
- **Showtime Scheduling:** Add showtimes with proper date and time validation.
- **Availability Controls:** Adjust pricing and available seats for individual showtimes dynamically.

---

## 🛠️ Database Schema

The database `movies.db` is built using **SQLite** and contains four core tables.

### 1. `Movies`

| Column Name | Type | Key / Attribute |
|---|---|---|
| `movie_id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `title` | TEXT | NOT NULL |
| `genre` | TEXT | |
| `duration` | INTEGER | In minutes |
| `info` | TEXT | Synopsis / Description |
| `cast` | TEXT | Cast members |

### 2. `Showtimes`

| Column Name | Type | Key / Attribute |
|---|---|---|
| `showtime_id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `movie_id` | INTEGER | FOREIGN KEY REFERENCES Movies(movie_id) |
| `time` | TEXT | Formatted showtime |
| `available_seats` | INTEGER | |
| `price` | REAL | Cost per ticket |

### 3. `Seats`

| Column Name | Type | Key / Attribute |
|---|---|---|
| `seat_id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `showtime_id` | INTEGER | FOREIGN KEY REFERENCES Showtimes(showtime_id) |
| `seat_number` | TEXT | Example: S1, S2 |
| `is_booked` | INTEGER | 0 = Available, 1 = Booked |

### 4. `Bookings`

| Column Name | Type | Key / Attribute |
|---|---|---|
| `booking_id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `showtime_id` | INTEGER | FOREIGN KEY REFERENCES Showtimes(showtime_id) |
| `customer_name` | TEXT | |
| `num_tickets` | INTEGER | |
| `total_price` | REAL | |
| `seats` | TEXT | Comma-separated seat numbers |

---

## 📁 File Architecture

- **`app.py`**: Manages database connections and application configuration.
- **`main.py`**: Main entry point for the Streamlit application.
- **`booking.py`**: Handles movie booking and seat selection logic.
- **`admin.py`**: Contains the admin dashboard and management functions.
- **`create_db.py`**: Creates the SQLite database and initializes tables.
- **`update_db.py`**: Updates database structure.
- **`update_bookings.py`**: Updates booking-related database fields.
- **`update_movies_table.py`**: Updates the Movies table.

---

## 💻 Setup & Installation Instructions

### Prerequisites

- Python 3.8+
- pip package manager
- Streamlit

### 1. Clone the Repository

```bash
cd Movie-Ticket

###  2. Install Dependencies

Make sure you have Streamlit installed:

````bash
pip install streamlit

### 3. Initialize the Database

Run the setup files to configure database tables and columns:

````bash
python create_db.py
python update_db.py
python update_bookings.py
python update_movies_table.py


### 4. Run the Application

Start the Streamlit application server:

````bash
streamlit run main.py
After execution, a browser tab should automatically open at http://localhost:8501.
