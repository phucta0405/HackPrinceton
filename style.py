import streamlit as st

def apply_custom_styles():
    st.markdown(
        """
        <style>
        /* Global CSS */
        .stApp {
            background-color: #f9f9f9;
            font-family: Arial, sans-serif;
        }
        /* Header Styling */
        .main-header {
            font-size: 2em;
            color: #1E90FF;
            margin-bottom: 20px;
        }
        /* Link Styles */
        .nav-link {
            display: inline-block;
            padding: 10px 20px;
            margin: 0 10px;
            background-color: #1E90FF;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        .nav-link:hover {
            background-color: #005bb5;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
