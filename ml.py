import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

# Set page configuration
st.set_page_config(page_title="Small Business Financial Wellness App", layout="centered")

# Title and Description
st.title("📈 Predictive Models on Financial Plans")
st.markdown(
    """
    **Monitor and improve your company’s financial health**  
    Track essential metrics, set financial goals, and visualize your progress.
    """
)

# Load or initialize the dataset
DATA_FILE = "financial_data.csv"

# Load data if file exists
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    # Initialize with some sample data
    data = {
        'Month': ['January 2024', 'February 2024', 'March 2024', 'April 2024'],
        'Savings ($)': [1000, 5000, 10000, 20000],
        'Debt ($)': [500, 1500, 1000, 2500],
        'Expenses ($)': [1000, 2000, 1500, 3000],
        'Income ($)': [5000, 15000, 20000, 25000]
    }
    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, index=False)  # Save the initial dataset to a file

# Add columns for Year and Month to help with sorting
df['Year'] = pd.to_datetime(df['Month'], format='%B %Y').dt.year
df['Month_Num'] = pd.to_datetime(df['Month'], format='%B %Y').dt.month

# Sort by Year first, then by Month
df = df.sort_values(by=['Year', 'Month_Num'], ascending=[True, True])

# Financial Input Section
st.header("Enter Financial Information")

# Arrange inputs in two columns
col1, col2 = st.columns(2)

with col1:
    income = st.number_input("Monthly Revenue ($)", min_value=0.0, format="%.2f", help="Your total monthly income from all revenue streams.")
    savings = st.number_input("Total Cash Reserve ($)", min_value=0.0, format="%.2f", help="Current amount in cash reserves.")

with col2:
    debt = st.number_input("Monthly Debt Payments ($)", min_value=0.0, format="%.2f", help="Total monthly payments towards business debt.")
    expenses = st.number_input("Monthly Operating Expenses ($)", min_value=0.0, format="%.2f", help="Total monthly business operating costs.")

# Placeholder for ML Model Input
st.header("Income Prediction")

# Function to predict income based on historical data and the model
def predict_income(savings, debt, expenses, df):
    # Feature matrix (X) and target (y)
    X = df[['Savings ($)', 'Debt ($)', 'Expenses ($)']]
    y = df['Income ($)']
    
    # Fit a linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict income based on user input
    prediction = model.predict(np.array([[savings, debt, expenses]]))
    return prediction[0]

# Predict income based on the user inputs and display it
predicted_income = predict_income(savings, debt, expenses, df)
st.write(f"**Predicted Monthly Income: ${predicted_income:,.2f}**")

# Recommendation based on prediction
if predicted_income < 5000:
    st.warning("Your predicted income is low. Consider reducing expenses or increasing revenue through marketing or new product offerings.")
elif 5000 <= predicted_income < 15000:
    st.success("Your income is on track! Focus on optimizing cash flow and reducing unnecessary expenses.")
else:
    st.success("Your business is doing great! Consider expanding and diversifying revenue streams for further growth.")

# Data Table Section
st.header("Current Financial Data")

# Display the current data table, now sorted by Year and Month
st.dataframe(df)

# Input for new data with month and year dropdown
st.header("Add New Financial Data")

# Dropdown menu for month
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month = st.selectbox("Select Month", months)

# Dropdown menu for year
current_year = 2024  # Example: You can set this dynamically or manually
years = [year for year in range(current_year - 10, current_year + 1)]  # Past 10 years to current year
year = st.selectbox("Select Year", years)

# Input fields for financial data
new_savings = st.number_input("Savings ($)", min_value=0.0, format="%.2f")
new_debt = st.number_input("Debt ($)", min_value=0.0, format="%.2f")
new_expenses = st.number_input("Expenses ($)", min_value=0.0, format="%.2f")

# Button to add the new data and update the model
if st.button("Add Data"):
    if month and year and new_savings and new_debt and new_expenses:
        # Add new data to the DataFrame
        new_data = pd.DataFrame({
            'Month': [f"{month} {year}"],
            'Savings ($)': [new_savings],
            'Debt ($)': [new_debt],
            'Expenses ($)': [new_expenses],
            'Income ($)': [predict_income(new_savings, new_debt, new_expenses, df)],  # Predict income based on the new data
        })
        
        # Append to the existing data
        df = pd.concat([df, new_data], ignore_index=True)
        
        # Add Year and Month_Num for sorting
        df['Year'] = pd.to_datetime(df['Month'], format='%B %Y').dt.year
        df['Month_Num'] = pd.to_datetime(df['Month'], format='%B %Y').dt.month

        # Sort by Year first, then by Month
        df = df.sort_values(by=['Year', 'Month_Num'], ascending=[True, True])
        
        # Save the updated data to the file
        df.to_csv(DATA_FILE, index=False)
        
        # Display updated table
        st.dataframe(df)
        
        # Retrain the model with the updated dataset
        predicted_income = predict_income(new_savings, new_debt, new_expenses, df)
        st.write(f"**Updated Predicted Monthly Income: ${predicted_income:,.2f}**")
        
        st.success(f"Data for {month} {year} added successfully!")
    else:
        st.error("Please fill all the fields before adding data.")

# Remove Data Section
st.header("Remove Financial Data")

# Dropdown to select the month and year to remove
remove_month = st.selectbox("Select Month to Remove", months)
remove_year = st.selectbox("Select Year to Remove", years)

# Button to remove the selected data
if st.button("Remove Data"):
    if remove_month and remove_year:
        # Create a month-year string to match the data
        month_year_str = f"{remove_month} {remove_year}"
        
        # Remove the data matching the selected month and year
        df = df[df['Month'] != month_year_str]
        
        # Save the updated DataFrame
        df.to_csv(DATA_FILE, index=False)
        
        # Display updated table
        st.dataframe(df)
        
        st.success(f"Data for {month_year_str} removed successfully!")
    else:
        st.error("Please select both a month and year to remove data.")

# Visualization Section
st.header("Financial Data Visualization")

# Plotting savings over time
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Month'], df['Savings ($)'], marker='o', label="Savings")
ax.plot(df['Month'], df['Income ($)'], marker='o', label="Income")
ax.set_xlabel("Month")
ax.set_ylabel("Amount ($)")
ax.set_title("Business Financial Health Over Time")
ax.legend()
st.pyplot(fig)

# Goal Setting Section
st.header("Set Financial Goals")

goal_savings = st.number_input("Set Savings Goal ($)", min_value=0.0, format="%.2f")
goal_income = st.number_input("Set Income Goal ($)", min_value=0.0, format="%.2f")

if st.button("Set Goals"):
    if goal_savings > 0 and goal_income > 0:
        st.success(f"Your financial goals are set!\n- Savings Goal: ${goal_savings:,.2f}\n- Income Goal: ${goal_income:,.2f}")
    else:
        st.error("Please set both savings and income goals.")
