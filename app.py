from nav import Nav
import streamlit as st


# Set up navigation with st.page for accessing external .py files
navigation = Nav(
    [
        st.Page('home.py', title="Home"),
        st.Page('finance_help.py', title="Finance Help"),
        st.Page('ml.py', title="Predictive Models"),
        st.Page('taxestimator.py', title="Tax Estimator"),
        st.Page('chatbot.py', title="Chatbot"),
        st.Page('humanhelp.py', title="Request Help")

    ]
)
