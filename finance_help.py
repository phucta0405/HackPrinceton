import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Small Business Financial Wellness App", layout="centered")

# Title and Description
st.title("📈 Small Business Financial Wellness App")
st.markdown(
    """
    **Monitor and improve your company’s financial health**  
    Track essential metrics, set financial goals, and visualize your progress—all tailored for small businesses.
    """
)

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

# Key Metrics Calculation with Edge Handling
if income > 0:
    debt_to_income_ratio = (debt / income) * 100
    savings_rate = (savings / (income * 12)) * 100
else:
    debt_to_income_ratio = savings_rate = 0

# Emergency Fund Calculation
emergency_fund_months = (savings / expenses) if expenses > 0 else float('inf') if savings > 0 else 0

# Display Financial Summary in Columns
st.header("Financial Health Overview")

col3, col4, col5 = st.columns(3)

# Debt-to-Income Ratio
with col3:
    st.subheader("Debt-to-Income Ratio")
    st.write(f"**{debt_to_income_ratio:.2f}%**")
    if debt_to_income_ratio < 15:
        st.success("Healthy debt-to-income ratio.")
    elif 15 <= debt_to_income_ratio <= 36:
        st.warning("Moderate debt-to-income ratio.")
    else:
        st.error("High debt-to-income ratio.")

# Savings Rate
with col4:
    st.subheader("Savings Rate")
    st.write(f"**{savings_rate:.2f}%**")
    if savings_rate >= 20:
        st.success("Good savings reserve.")
    elif 10 <= savings_rate < 20:
        st.warning("Moderate savings reserve.")
    else:
        st.error("Low savings rate.")

# Emergency Fund
with col5:
    st.subheader("Emergency Fund")
    if emergency_fund_months == float('inf'):
        st.write("**More than sufficient!**")
        st.success("Excellent emergency fund!")
    else:
        st.write(f"**{emergency_fund_months:.2f} months**")
        if emergency_fund_months >= 6:
            st.success("Solid emergency fund.")
        elif 3 <= emergency_fund_months < 6:
            st.warning("Consider increasing emergency reserves.")
        else:
            st.error("Low emergency reserves.")

# Revenue and Expense Breakdown
st.header("Financial Visualizations")

# Income Allocation Pie Chart
st.subheader("Revenue Allocation")
remaining_income = max(income - (debt + expenses), 0)
allocation = np.array([debt, expenses, remaining_income])
labels = ['Debt Payments', 'Operating Expenses', 'Remaining Income']
if allocation.sum() > 0:
    fig, ax = plt.subplots()
    ax.pie(allocation, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.write("No income allocation data to display.")

# Monthly vs Annual Savings Bar Chart
st.subheader("Monthly vs Annual Cash Reserve Growth")
monthly_savings = max(income - (debt + expenses), 0)
annual_savings = monthly_savings * 12
if monthly_savings > 0:
    savings_df = pd.DataFrame({'Amount': [monthly_savings, annual_savings]},
                              index=['Monthly Savings', 'Annual Savings'])
    st.bar_chart(savings_df)
else:
    st.write("No cash reserve data to display.")

# Cash Flow Forecasting for 5 Years
st.subheader("Projected Cash Reserve Growth (5 Years)")
months = np.arange(1, 61)
projected_savings = np.cumsum(np.full_like(months, monthly_savings))
if monthly_savings > 0:
    growth_df = pd.DataFrame({'Month': months, 'Projected Savings ($)': projected_savings})
    st.line_chart(growth_df.set_index('Month'))
else:
    st.write("No projected growth data to display.")

# Financial Ratios Section
st.header("Advanced Financial Ratios")

col6, col7 = st.columns(2)
with col6:
    st.subheader("Gross Profit Margin")
    gross_profit = st.number_input("Gross Profit ($)", min_value=0.0, format="%.2f", help="Your total profit after cost of goods sold.")
    if income > 0:
        gross_profit_margin = (gross_profit / income) * 100
        st.write(f"**{gross_profit_margin:.2f}%**")
        if gross_profit_margin > 50:
            st.success("Excellent profit margin.")
        elif 20 <= gross_profit_margin <= 50:
            st.warning("Average profit margin.")
        else:
            st.error("Low profit margin.")
    else:
        st.write("Enter revenue data to calculate.")

with col7:
    st.subheader("Net Profit Margin")
    net_profit = income - expenses - debt
    net_profit_margin = (net_profit / income * 100) if income > 0 else 0
    st.write(f"**{net_profit_margin:.2f}%**")
    if net_profit_margin > 15:
        st.success("Healthy net profit margin.")
    elif 5 <= net_profit_margin <= 15:
        st.warning("Moderate net profit margin.")
    else:
        st.error("Low net profit margin.")

# Goal Setting Section
# Set Financial Goals Section
st.header("Set Financial Goals")

# Define minimum and maximum values for the revenue and cash reserve goals
revenue_goal_min = 0
revenue_goal_max = int(income * 12 * 2) if income > 0 else 0
cash_goal_max = int(savings * 2) if savings > 0 else 0

# Set financial goals only if valid ranges are available
if revenue_goal_max > revenue_goal_min:
    revenue_goal = st.slider("Annual Revenue Goal ($)", min_value=revenue_goal_min, max_value=revenue_goal_max, 
                             value=int(income * 12 * 1.5), help="Set your target for annual revenue.")
else:
    st.write("No revenue goal data to display.")

if cash_goal_max > 0:
    cash_goal = st.slider("Target Cash Reserve ($)", min_value=0, max_value=cash_goal_max, 
                          value=int(savings * 1.5), help="Set a target cash reserve for your emergency fund.")
else:
    st.write("No cash reserve goal data to display.")

# Display progress toward financial goals if applicable
st.subheader("Progress Towards Goals")

# Projected Annual Revenue Calculation
annual_revenue_projection = income * 12
if revenue_goal_max > 0:
    st.write(f"Projected Annual Revenue: **${annual_revenue_projection:,.2f}**")
    if annual_revenue_projection >= revenue_goal:
        st.success("On track to meet revenue goal!")
    else:
        st.warning(f"Additional revenue needed to meet goal: ${revenue_goal - annual_revenue_projection:,.2f}")
else:
    st.write("No revenue projection data to display.")

# Cash Reserve Goal Calculation
if cash_goal_max > 0:
    st.write(f"Projected Cash Reserve: **${savings:,.2f}**")
    if savings >= cash_goal:
        st.success("Cash reserve goal achieved!")
    else:
        st.warning(f"Additional savings needed to meet goal: ${cash_goal - savings:,.2f}")
else:
    st.write("No cash reserve projection data to display.")
