import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Financial Wellness Calculator", layout="centered")

# Title
st.title("💸 Financial Wellness Calculator")

# Input section
st.header("Enter your financial information")

# Arrange inputs in two columns
col1, col2 = st.columns(2)

with col1:
    income = st.number_input("Monthly Income ($)", min_value=0.0, format="%.2f")
    savings = st.number_input("Total Savings ($)", min_value=0.0, format="%.2f")

with col2:
    debt = st.number_input("Monthly Debt Payments ($)", min_value=0.0, format="%.2f")
    expenses = st.number_input("Monthly Expenses ($)", min_value=0.0, format="%.2f")

# Calculate Financial Ratios with Edge Case Handling
if income > 0:
    debt_to_income = (debt / income) * 100
    savings_rate = (savings / (income * 12)) * 100
else:
    debt_to_income = savings_rate = 0  # Avoid division by zero

# Avoid division by zero for emergency fund months calculation
emergency_fund_months = (savings / expenses) if expenses > 0 else float('inf') if savings > 0 else 0

# Display Results in Columns
st.header("Your Financial Wellness Summary")

# Arrange results in three columns
col3, col4, col5 = st.columns(3)

with col3:
    st.subheader("Debt-to-Income Ratio")
    st.write(f"**{debt_to_income:.2f}%**")
    if debt_to_income < 15:
        st.success("Healthy debt-to-income ratio.")
    elif 15 <= debt_to_income <= 36:
        st.warning("Moderate debt-to-income ratio.")
    else:
        st.error("High debt-to-income ratio.")

with col4:
    st.subheader("Savings Rate")
    st.write(f"**{savings_rate:.2f}%**")
    if savings_rate >= 20:
        st.success("Strong savings habit.")
    elif 10 <= savings_rate < 20:
        st.warning("Decent savings rate.")
    else:
        st.error("Low savings rate.")

with col5:
    st.subheader("Emergency Fund")
    if emergency_fund_months == float('inf'):
        st.write("**More than enough!**")
        st.success("Excellent emergency fund!")
    else:
        st.write(f"**{emergency_fund_months:.2f} months**")
        if emergency_fund_months >= 6:
            st.success("Solid emergency fund!")
        elif 3 <= emergency_fund_months < 6:
            st.warning("Consider increasing emergency fund.")
        else:
            st.error("Low emergency fund.")

# Graphs
st.header("Financial Wellness Visualizations")

# Pie Chart: Income Allocation with Edge Case Handling
st.subheader("Income Allocation")
remaining_income = max(income - (debt + expenses), 0)  # Prevents negative remaining income
income_allocation = np.array([debt, expenses, remaining_income])
labels = ['Debt', 'Expenses', 'Remaining Income']
fig, ax = plt.subplots()
ax.pie(income_allocation, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig)

# Bar Chart: Monthly vs Annual Savings with Edge Case Handling
st.subheader("Monthly vs Annual Savings")
monthly_savings = max(income - (debt + expenses), 0)  # Prevent negative monthly savings
annual_savings = monthly_savings * 12
savings_df = pd.DataFrame(
    {'Amount': [monthly_savings, annual_savings]},
    index=['Monthly Savings', 'Annual Savings']
)
st.bar_chart(savings_df)

# Line Chart: Projected Savings Growth Over 5 Years with Edge Case Handling
st.subheader("Projected Savings Growth (5 Years)")
months = np.arange(1, 61)  # 5 years in months
projected_savings = np.cumsum(np.full_like(months, monthly_savings))
savings_growth_df = pd.DataFrame({
    'Month': months,
    'Projected Savings ($)': projected_savings
})
st.line_chart(savings_growth_df.set_index('Month'))

# Footer
st.caption("Use this tool to assess your financial wellness and set goals for improvement.")
