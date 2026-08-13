import streamlit as st
import time
import random
from booking import get_movies, get_showtimes, book_ticket,get_seats,initialize_seats
from admin import admin_panel

st.title("🎟️ Movie Ticket Booking System")

st.set_page_config(
    page_title="Movie Ticket",        # Title shown in browser tab
    page_icon="🎬",             # Icon shown in browser tab
    layout="wide",              # "centered" or "wide"
    initial_sidebar_state="expanded"  # "expanded" or "collapsed"
)

st.markdown(""" 
<style>  
.stApp {
    background-color: #1C0C2B;
    color: #F0F0F0;
}
.stButton>button {
    background-color: #FF007F;
    color: white;
}
.stButton>button:hover {
    background-color: #B20710;
    color: white;
}
</style>
""", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu", ["User", "Admin"])

if menu == "User":
    movies = get_movies()     # movie_id, title, genre, duration, info, cast
    movie_dict = {m[1]: m[0] for m in movies}

    # Dropdown shows only movie titles
    movie_selected = st.selectbox("Select Movie", list(movie_dict.keys()))
    movie_id = movie_dict[movie_selected]

    # Get full data for selected movie
    selected_movie = next(m for m in movies if m[0] == movie_id)
    _, title, genre, duration, info, cast = selected_movie
    #for m in movies: 
    #  if m[0] == movie_id:
    #   this movie matches the selected movie_id
    #  selected_movie = (1, "Avengers", "Action", 180, "Earth's mightiest heroes...", "RDJ, Chris Evans")
    #_ (movie_id) – we use _ because we don’t need it)
    

    # Display movie details after selection
    st.markdown("### 🎬 Movie Details")
    st.write(f"**Title:** {title}")
    st.write(f"**Genre:** {genre}")
    st.write(f"**Description:** {info}")
    st.write(f"**Cast:** {cast}")

   
    showtimes = get_showtimes(movie_id)

    if showtimes:
        show = st.selectbox(
            "Select Showtime",
            showtimes,
            format_func=lambda x: f"ID {x[0]} | {x[2]} | Seats: {x[3]} | Price: ₹{x[4]}"
        )
    else:
        st.warning("⚠️ No showtimes available for this movie")
        st.stop()

    name = st.text_input("Your Name")


# Initialize seats for the showtime (only first time)
    initialize_seats(show[0], show[3])  # show[3] = available_seats from Showtimes

    seats = get_seats(show[0])

    st.markdown("### Select Seats:")



    if 'selected_seats' not in st.session_state:
        st.session_state.selected_seats = []


    cols = st.columns(10)  # 10 seats per row
    for idx, (seat_number, is_booked) in enumerate(seats):
        col = cols[idx % 10]
        if is_booked:
            col.button(seat_number, disabled=True, key=f"{seat_number}_booked")
        else:
            if col.button(seat_number, key=f"{seat_number}_avail"):
                if seat_number not in st.session_state.selected_seats:
                    st.session_state.selected_seats.append(seat_number)

    st.write("Selected Seats:", st.session_state.selected_seats)

    # ---------------- PAYMENT SECTION ---------------- #

    if st.session_state.selected_seats:

        # Calculate total amount
        total_amount = len(st.session_state.selected_seats) * show[4]
        st.markdown(f"### 💰 Total Amount: ₹{total_amount}")

        # Payment method selection
        payment_method = st.selectbox(
            "Select Payment Method",
            ["UPI", "Credit/Debit Card", "Net Banking"]
        )

        # Show fake payment fields
        if payment_method == "UPI":
            upi_id = st.text_input("Enter UPI ID")

        elif payment_method == "Credit/Debit Card":
            card_number = st.text_input("Card Number")
            expiry = st.text_input("Expiry (MM/YY)")
            cvv = st.text_input("CVV", type="password")

        elif payment_method == "Net Banking":
            bank = st.selectbox("Select Bank", ["SBI", "HDFC", "ICICI", "Axis"])

        # Payment button
        if st.button("Proceed to Pay"):
            if name == "":
                st.warning("Please enter your name")

            else:
                payment_success = False  # default

            # -------- UPI VALIDATION --------
            if payment_method == "UPI":
                if upi_id and "@" in upi_id and len(upi_id) >= 5:
                    payment_success = True
                else:
                    st.error("Invalid UPI ID")

            # -------- CARD VALIDATION --------
            elif payment_method == "Credit/Debit Card":
                if (card_number.isdigit() and len(card_number) == 16 and cvv.isdigit() and len(cvv) == 3 and
                    len(expiry) == 5 and expiry[2] == "/"):
                    payment_success = True
                else:
                    st.error("Invalid Card Details")

            # -------- NET BANKING VALIDATION --------
            elif payment_method == "Net Banking":
                if bank:
                    payment_success = True

            # -------- PROCESS PAYMENT --------
            if payment_success:
                with st.spinner("🔄 Processing Payment..."):
                    time.sleep(2)

                result = book_ticket(show[0], name, st.session_state.selected_seats)

                if result:
                    st.success("✅ Payment Successful!")
                    st.success("🎉 Booking Confirmed!")

                    st.write("👤 Name:", name)
                    st.write("🎟 Seats:", st.session_state.selected_seats)
                    st.write("💵 Amount Paid: ₹", result)
                    st.write("🧾 Transaction ID:", "TXN" + str(random.randint(100000, 999999)))

                    st.session_state.selected_seats = []
                else:
                    st.error("Some seats were already booked!")


    

else:
    admin_panel()

