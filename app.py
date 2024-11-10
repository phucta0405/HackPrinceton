import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
import bcrypt
from nav import *
# Path to YAML file
DB_FILE = Path("db.yaml")

# Load YAML data
def load_db():
    with open('db.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config


# Save data to YAML
def save_db(data):
    with open(DB_FILE, "w") as file:
        yaml.dump(data, file)

# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Initialize authenticator
def init_authenticator():
    return stauth.Authenticate(load_db(), "app", "abcdef", cookie_expiry_days=1)

def login_redirect():
    st.session_state["active_tab"] = "Login"

# User registration
def register_user(name, username, email, password):
    db = load_db()
    if username in db["usernames"]:
        st.error("Username already exists!")
        return False
    db["usernames"][username] = {
        "name": name,
        "email": email,
        "password": hash_password(password),
    }
    save_db(db)
    st.success("User registered successfully!")
    login_redirect()
    return True

# Login page redirection


# Main app
def main():
    # Tabs for login and registration
    tab1, tab2 = st.tabs(["Register", "Login"])
    # Registration tab
    with tab1:
        st.header("Register New User")
        new_name = st.text_input("Name")
        new_username = st.text_input("Username")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        new_password_confirm = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if new_password == new_password_confirm:
                register_user(new_name, new_username, new_email, new_password)
                login_redirect()  # Redirect to login after successful registration
            else:
                st.error("Passwords do not match")

    # Login tab
    with tab2:
        authenticator = init_authenticator()
        authenticator.login()

        if st.session_state["authentication_status"]:
            authenticator.logout()
            st.write(f'Welcome *{st.session_state["name"]}*')
            navigation = Nav(
                [
                    st.Page('home.py', title="Home"),
                    st.Page('finance_help.py', title="Finance Help"),
                    st.Page('ml.py', title="Predictive Models"),
                    st.Page('tax_estimator.py', title="Tax Estimator"),
                    st.Page('chatbot.py', title="Chatbot"),
                    st.Page('humanhelp.py', title="Request Help"),
                    st.Page('taxfilling.py', title="NEW | Individual Tax Filling")
                ]
            )
            # enter the rest of the streamlit app here
        elif st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')

if __name__ == "__main__":
    main()