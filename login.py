import streamlit as st
import hashlib

# In-memory storage for user data (for demonstration purposes)
# In a real application, consider using a database to store user credentials securely.
users_db = {}

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Registration function
def register_user(username, password):
    if username in users_db:
        st.warning("Username already taken!")
    else:
        users_db[username] = hash_password(password)
        st.success("User registered successfully! Please log in.")



# Login function
def login_user(username, password):
    if username not in users_db:
        st.warning("User does not exist!")
    elif users_db[username] != hash_password(password):
        st.warning("Incorrect password!")
    else:
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.success(f"Welcome, {username}!")
        st.switch_page("driver.py")

# Logout function
def logout_user():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.success("You have been logged out.")

# Main app layout
def main():
    st.title("Login Page")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = None

    if st.session_state['logged_in']:
        st.subheader(f"Hello, {st.session_state['username']}!")
        if st.button("Logout"):
            logout_user()
    else:
         option = st.selectbox("Choose an option", ["Login", "Register"])
         if option == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                login_user(username, password)

            elif option == "Register":
                st.subheader("Register")
                new_username = st.text_input("Choose a Username")
                new_password = st.text_input("Choose a Password", type="password")

            if st.button("Register"):
                register_user(new_username, new_password)

main()
        
