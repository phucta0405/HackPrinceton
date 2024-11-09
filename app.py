from nav import Nav
import streamlit as st

def support():
    st.title("Request Human Help")

# Set up navigation with st.page for accessing external .py files
navigation = Nav(
    [st.Page('home.py'),
    st.Page('finance_help.py'),
    st.Page('tax_estimator.py'),
     st.Page("chatbot.py"),
     st.Page(support)]
)