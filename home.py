import streamlit as st

# Set page configuration
# st.set_page_config(page_title="Home Page", layout="centered")

def show_home():
    st.image("logo.png", width=400)
    st.title("🏠 Home Page")
    st.write("Welcome to the **Home Page**. Explore the Pennyworth's features and get started on your journey to financial wellness.")
show_home()

st.title("Welcome to the Financial Wellness App 💸")

st.header("Your Financial Journey Starts Here")
st.write("""
        Welcome to our Financial Wellness App! This tool is designed to help you better understand your finances 
        by calculating important metrics like your debt-to-income ratio, savings rate, and emergency fund status.
    """)

st.write("""
        ### Key Features:
        - **Financial Wellness Calculator**: A comprehensive tool to analyze your monthly income, debt, expenses, and savings.
        - **Projected Savings Growth**: See how your savings can grow over time based on your monthly contributions.
        - **Debt-to-Income Ratio**: A measure of your 
        financial health, based on your income versus your debt.

        Take control of your financial future with us!
    """)
st.write("### Ready to take the next step?")
st.button("Start Calculating Your Financial Wellness", on_click=lambda: st.Page('finance_help.py'))

st.header("About Our App")
st.write("""
        Our mission is to help individuals understand their financial health and make smarter decisions.
        This app provides easy-to-use tools to analyze income, debt, expenses, savings, and more.
    """)

st.header("Contact Us")
st.write("""
        If you have any questions or feedback, feel free to reach out:
    """)
st.write("Email: contact@financialwellnessapp.com")
st.write("Phone: +1 (800) 123-4567")

