import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

st.set_page_config(page_title="Small Business Financial Wellness App", layout="centered")
st.title("📈 Predictive Models on Financial Plans")
st.markdown(
    """
    **Monitor and improve your company’s financial health**  
    Track essential metrics, set financial goals, and visualize your progress.
    """
)
DATA_FILE = "financial_data.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    data = {
        'Month': ['January 2024', 'February 2024', 'March 2024', 'April 2024'],
        'Savings ($)': [1000, 5000, 10000, 20000],
        'Debt ($)': [500, 1500, 1000, 2500],
        'Expenses ($)': [1000, 2000, 1500, 3000],
        'Income ($)': [5000, 15000, 20000, 25000]
    }
    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, index=False)
df['Year'] = pd.to_datetime(df['Month'], format='%B %Y').dt.year
df['Month_Num'] = pd.to_datetime(df['Month'], format='%B %Y').dt.month
df = df.sort_values(by=['Year', 'Month_Num'], ascending=[True, True])

st.header("Enter Financial Information")

col1, col2 = st.columns(2)

with col1:
    income = st.number_input("Monthly Revenue ($)", min_value=0.0, format="%.2f", help="Your total monthly income from all revenue streams.")
    savings = st.number_input("Total Cash Reserve ($)", min_value=0.0, format="%.2f", help="Current amount in cash reserves.")

with col2:
    debt = st.number_input("Monthly Debt Payments ($)", min_value=0.0, format="%.2f", help="Total monthly payments towards business debt.")
    expenses = st.number_input("Monthly Operating Expenses ($)", min_value=0.0, format="%.2f", help="Total monthly business operating costs.")

st.header("Income Prediction")

def predict_income(savings, debt, expenses, df):
    X = df[['Savings ($)', 'Debt ($)', 'Expenses ($)']]
    y = df['Income ($)']
    model = LinearRegression()
    model.fit(X, y)
    prediction = model.predict(np.array([[savings, debt, expenses]]))
    return prediction[0]
predicted_income = predict_income(savings, debt, expenses, df)
st.write(f"**Predicted Monthly Income: ${predicted_income:,.2f}**")

if predicted_income < 5000:
    st.warning("Your predicted income is low. Consider reducing expenses or increasing revenue through marketing or new product offerings.")
elif 5000 <= predicted_income < 15000:
    st.success("Your income is on track! Focus on optimizing cash flow and reducing unnecessary expenses.")
else:
    st.success("Your business is doing great! Consider expanding and diversifying revenue streams for further growth.")
st.header("Current Financial Data")

st.dataframe(df)
st.header("Add New Financial Data")
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month = st.selectbox("Select Month", months)
current_year = 2024 
years = [year for year in range(current_year - 10, current_year + 1)] 
year = st.selectbox("Select Year", years)

new_savings = st.number_input("Savings ($)", min_value=0.0, format="%.2f")
new_debt = st.number_input("Debt ($)", min_value=0.0, format="%.2f")
new_expenses = st.number_input("Expenses ($)", min_value=0.0, format="%.2f")

if st.button("Add Data"):
    if month and year and new_savings and new_debt and new_expenses:
        new_data = pd.DataFrame({
            'Month': [f"{month} {year}"],
            'Savings ($)': [new_savings],
            'Debt ($)': [new_debt],
            'Expenses ($)': [new_expenses],
            'Income ($)': [predict_income(new_savings, new_debt, new_expenses, df)], 
        })
        df = pd.concat([df, new_data], ignore_index=True)
        df['Year'] = pd.to_datetime(df['Month'], format='%B %Y').dt.year
        df['Month_Num'] = pd.to_datetime(df['Month'], format='%B %Y').dt.month
        df = df.sort_values(by=['Year', 'Month_Num'], ascending=[True, True])
        df.to_csv(DATA_FILE, index=False)
        st.dataframe(df)
        predicted_income = predict_income(new_savings, new_debt, new_expenses, df)
        st.write(f"**Updated Predicted Monthly Income: ${predicted_income:,.2f}**")
        
        st.success(f"Data for {month} {year} added successfully!")
    else:
        st.error("Please fill all the fields before adding data.")

st.header("Remove Financial Data")
remove_month = st.selectbox("Select Month to Remove", months)
remove_year = st.selectbox("Select Year to Remove", years)
if st.button("Remove Data"):
    if remove_month and remove_year:
        month_year_str = f"{remove_month} {remove_year}"
        df = df[df['Month'] != month_year_str]
        df.to_csv(DATA_FILE, index=False)
        st.dataframe(df)
        
        st.success(f"Data for {month_year_str} removed successfully!")
    else:
        st.error("Please select both a month and year to remove data.")
st.header("Financial Data Visualization")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Month'], df['Savings ($)'], marker='o', label="Savings")
ax.plot(df['Month'], df['Income ($)'], marker='o', label="Income")
ax.set_xlabel("Month")
ax.set_ylabel("Amount ($)")
ax.set_title("Business Financial Health Over Time")
ax.legend()
st.pyplot(fig)
st.header("Set Financial Goals")

goal_savings = st.number_input("Set Savings Goal ($)", min_value=0.0, format="%.2f")
goal_income = st.number_input("Set Income Goal ($)", min_value=0.0, format="%.2f")

if st.button("Set Goals"):
    if goal_savings > 0 and goal_income > 0:
        st.success(f"Your financial goals are set!\n- Savings Goal: ${goal_savings:,.2f}\n- Income Goal: ${goal_income:,.2f}")
    else:
        st.error("Please set both savings and income goals.")
