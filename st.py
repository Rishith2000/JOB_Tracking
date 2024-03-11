import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256
import datetime

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def verify_password(password, hashed_password):
    return pbkdf2_sha256.verify(password, hashed_password)

def create_tables():
    conn = sqlite3.connect('job_tracker.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company_name TEXT NOT NULL,
            position TEXT NOT NULL,
            application_date DATE,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

def main():
    create_tables()

    conn = sqlite3.connect('job_tracker.db')
    c = conn.cursor()


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
if st.button("Sign Up"):
    try:
        # Existing code

        if existing_user:
            st.error("Username already exists. Please choose a different one.")
        else:
            hashed_password = hash_password(new_password)
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, hashed_password))
            conn.commit()
            st.success("Account created successfully. You can now log in.")

            # Git commit to track the user sign-up
            os.system("git add job_tracker.db")
            os.system("git commit -m 'User sign-up: {}'".format(new_username))
            os.system("git push origin master")  # Push changes to GitHub
    except Exception as e:
        st.error(f"Error during sign-up: {e}")


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
