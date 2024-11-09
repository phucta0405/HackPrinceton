from nav import Nav
import streamlit as st


def support():
    st.title("request Human Help")
   
navigation = Nav(
    [st.Page('home.py'),
        st.Page('finance_help.py'),
     st.Page("chatbot.py"),
     st.Page(support)]
     )


# In-memory storage for user data (for demonstration purposes)
# In a real application, consider using a database to store user credentials securely.
