import streamlit as st
import sqlite3
def get_connection():
    return sqlite3.connect("movies.db",check_same_thread=False)


# Every time your app needs data (movies, showtimes, bookings), it calls this function.”`
# “Allow different parts of my app (running in different threads) to use the same database connection.”`
#👉 In short:sqlite3.connect is like opening the door to your database file so your Python program can go inside, look at the tables, and change or read the data.\
#- Without check_same_thread=False → Streamlit might crash with errors when different parts of your app try to use the database.
# - With it → Your app can safely share the database connection across different parts (different threads).

# 👉 In short:
# - sqlite3.connect("movies.db") = open the database file so Python can use it.
# - check_same_thread=False = allow different parts of your app to share that same open connection.
# Would you like me to show you a tiny Streamlit example where one part of the app writes to the database and another part reads from it, so you can see why this option matters?

