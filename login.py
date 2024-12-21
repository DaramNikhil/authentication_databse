import sqlite3
import streamlit as st

def create_databases():
    """Initialize the database and create the users table if it doesn't exist."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def signup(user_name, password):
    """Register a new user in the database."""
    if not user_name or not password:
        return False, "Username and password cannot be empty."
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (user_name, password) VALUES (?, ?)", (user_name, password))
        conn.commit()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please try a different username."
    finally:
        conn.close()

def login(user_name, password):
    """Authenticate a user with the given credentials."""
    if not user_name or not password:
        return False
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_name = ? AND password = ?", (user_name, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

st.title("Authentication")
create_databases()

menu = ["Sign Up", "Login"]
selection = st.selectbox("Select", menu)

if selection == "Sign Up":
    st.subheader("Create a New Account")
    user_name = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")
    if st.button("Sign Up"):
        success, message = signup(user_name, password)
        if success:
            st.success(message)
        else:
            st.error(message)

elif selection == "Login":
    st.subheader("Login to Your Account")
    user_name = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")
    if st.button("Login"):
        if login(user_name, password):
            st.success("Successfully logged in!")
        else:
            st.error("Invalid credentials. Please try again.")
