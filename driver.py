from nav import Nav
import streamlit as st


def page1():
    st.write('test')
   
navigation = Nav(
    [st.Page('finance_help.py'),
     st.Page("chatbot.py")]
     )


# In-memory storage for user data (for demonstration purposes)
# In a real application, consider using a database to store user credentials securely.
