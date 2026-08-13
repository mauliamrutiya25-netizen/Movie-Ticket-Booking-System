import streamlit as st
from app import get_connection
from datetime import datetime   
def admin_panel():
    st.subheader("📊 Admin Dashboard")

    conn = get_connection()
    cur = conn.cursor()

    # ===================== METRICS =====================
    cur.execute("SELECT COUNT(*) FROM Bookings")
    st.metric("Total Bookings", cur.fetchone()[0])

    cur.execute("SELECT SUM(total_price) FROM Bookings")
    revenue = cur.fetchone()[0] #Get the first column of the first row returned by the query.
    st.metric("Total Revenue", f"₹{revenue}")

    st.divider()

    # ===================== MOVIE BOOKING REPORT =====================
    st.header("📄 Movie Booking Report")
    cur.execute("SELECT movie_id, title FROM Movies")
    movies = cur.fetchall()
    movie_map = {m[1]: m[0] for m in movies}
#m[0] first column movie id, m[1] second column title
    if movies:
        movie_selected = st.selectbox(
            "Select Movie to View Bookings",
            movie_map.keys(),       #movie title
            key="view_bookings"
        )
        movie_id = movie_map[movie_selected]

        cur.execute("""
            SELECT showtime_id, time, available_seats
            FROM Showtimes
            WHERE movie_id=?
        """, (movie_id,))
        showtimes = cur.fetchall()

        if showtimes:
            for show in showtimes:
                st.markdown(f"**Showtime:** {show[1]} | **Available Seats:** {show[2]}")
                
                cur.execute("""
                    SELECT customer_name, seats
                    FROM Bookings
                    WHERE showtime_id=?
                """, (show[0],))   #show[0] means showtime_id
                bookings = cur.fetchall()

                if bookings:
                    for b in bookings:
                        st.write(f"👤 {b[0]} → Seats: {b[1]}")     # name and seats
                else:
                    st.info("No bookings yet for this showtime")
        else:
            st.info("No showtimes available for this movie")

    st.divider()

    # ===================== ADD MOVIE =====================
    st.header("🎬 Add Movie")
    title = st.text_input("Movie Title", key="add_title")
    genre = st.text_input("Genre", key="add_genre")
    duration = st.number_input("Duration (minutes)", 60, 300, key="add_duration")
    info = st.text_area("Description", key="add_info")
    cast = st.text_area("Cast (comma-separated)", key="add_cast")

    if st.button("Add Movie", key="add_movie_btn"):
        if title.strip() == "":
            st.warning("Enter a movie title!")
        else:
            cur.execute(
                "INSERT INTO Movies (title, genre, duration, info, cast) VALUES (?, ?, ?, ?, ?)",
                (title, genre, duration, info, cast)
            )
            conn.commit()
            st.success(f"Movie '{title}' added successfully 🎉")

    st.divider()

    # ===================== DELETE MOVIE =====================
    st.header("🗑️ Delete Movie")
    if movies:
        movie_to_delete = st.selectbox(
            "Select Movie to Delete",
            movie_map.keys(),
            key="delete_movie"
        )
        if st.button("Delete Movie", key="delete_movie_btn"):
            cur.execute("DELETE FROM Showtimes WHERE movie_id=?", (movie_map[movie_to_delete],))
            cur.execute("DELETE FROM Movies WHERE movie_id=?", (movie_map[movie_to_delete],))
            conn.commit()
            st.success(f"Movie '{movie_to_delete}' deleted successfully")
    else:
        st.info("No movies available")

    st.divider()

    # ===================== MANAGE SHOWTIMES =====================
    st.header("⏰ Manage Showtimes")
    if movies:
        movie_for_showtime = st.selectbox(
            "Select Movie for Showtime",
            movie_map.keys(),
            key="manage_showtime"
        )
        time = st.text_input("Show Time (e.g. 2026-02-10 7:30 PM)", key="showtime_time")
        seats = st.number_input("Available Seats", 10, 300, key="showtime_seats")
        price = st.number_input("Ticket Price", 50, 1000, key="showtime_price")

    if st.button("Add Showtime", key="add_showtime_btn"):
            if time.strip() == "":
                st.warning("Add a valid showtime")
            else:
                try:
                    # Validate format: YYYY-MM-DD HH:MM AM/PM
                    valid_time = datetime.strptime(time, "%Y-%m-%d %I:%M %p")    # I means hour M means minutes , p means am or pm

                    cur.execute(
                        "INSERT INTO Showtimes (movie_id, time, available_seats, price) VALUES (?, ?, ?, ?)",
                        (movie_map[movie_for_showtime], time, seats, price)
                    )
                    conn.commit()
                    st.success("Showtime added successfully")

                except ValueError:
                    st.error("Invalid format! Use: YYYY-MM-DD HH:MM AM/PM (Example: 2026-02-10 07:30 PM)")


    else:
        st.info("Add movies first to manage showtimes")

    st.divider()

    # ===================== CONTROL TICKET AVAILABILITY =====================
    st.header("🎟️ Control Ticket Availability")
    cur.execute("SELECT showtime_id, time, available_seats, price FROM Showtimes")
    showtimes = cur.fetchall()

    if showtimes:
        show = st.selectbox(
            "Select Showtime to Update",
            showtimes,
            key="update_showtime_select",
            format_func=lambda x: f"ID {x[0]} | {x[1]} | Seats {x[2]} | ₹{x[3]}"
        )

        new_seats = st.number_input("Update Available Seats", 0, 500, show[2], key="update_seats")
        new_price = st.number_input("Update Price", 50, 1000, int(show[3]), key="update_price")

        if st.button("Update Showtime", key="update_showtime_btn"):
            cur.execute(
                "UPDATE Showtimes SET available_seats=?, price=? WHERE showtime_id=?",
                (new_seats, new_price, show[0])
            )
            conn.commit()
            st.success("Showtime updated successfully")
    else:
        st.info("No showtimes available")

    conn.close()



