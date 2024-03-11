import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256  # For password hashing

# Helper function to hash passwords
def hash_password(password):
    return pbkdf2_sha256.hash(password)

# Helper function to verify hashed passwords
def verify_password(password, hashed_password):
    return pbkdf2_sha256.verify(password, hashed_password)

# Streamlit app structure
def main():
    st.title("Job Application Tracker")

    # Create a database connection
    conn = sqlite3.connect('job_tracker.db')
    c = conn.cursor()

    # ... (Code for creating tables as shown in the previous response)

    # Navigation
    menu = ["Home", "Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to the Job Application Tracker App")

    elif choice == "Login":
        login(c)

    elif choice == "Sign Up":
        sign_up(c)

    conn.close()

# Login function
def login(c):
    st.subheader("Login Section")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Check if the user exists in the database
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()

        if user and verify_password(password, user[2]):
            st.success("Logged in as {}".format(username))
            # You can redirect the user to the job tracking section or perform other actions here
        else:
            st.error("Invalid username or password")

# Sign-up function
def sign_up(c):
    st.subheader("Create Account")

    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        # Check if the username already exists
        c.execute("SELECT * FROM users WHERE username=?", (new_username,))
        existing_user = c.fetchone()

        if existing_user:
            st.error("Username already exists. Please choose a different one.")
        else:
            # Add the new user to the database
            hashed_password = hash_password(new_password)
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, hashed_password))
            st.success("Account created successfully. You can now log in.")

# Streamlit app launch code
if __name__ == '__main__':
    main()