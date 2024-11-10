import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
st.set_page_config(page_title="Small Business Tax Deduction Estimator", layout="centered")
st.title("💼 Small Business Tax Deduction Estimator")
st.markdown(
    """
    **Optimize your tax planning with this deduction estimator**  
    Estimate your tax liabilities and identify potential tax savings based on deductible expenses. This tool is designed to help small business owners manage their taxes more effectively.
    """
)

st.header("Enter Your Tax Information")

col1, col2 = st.columns(2)
with col1:
    annual_income = st.number_input("Annual Revenue ($)", min_value=0.0, format="%.2f", help="Total annual revenue for tax estimation.")
    tax_rate = st.slider("Effective Tax Rate (%)", min_value=0.0, max_value=50.0, value=15.0, help="Estimated tax rate applicable to your business.")

with col2:
    deductible_expenses = st.number_input("Total Deductible Expenses ($)", min_value=0.0, format="%.2f", help="Sum of all deductible expenses.")
    other_tax_credits = st.number_input("Other Tax Credits ($)", min_value=0.0, format="%.2f", help="Other available tax credits.")
st.header("Deduction Categories")
deductions = {
    "Operational Costs": 0.0,
    "Salaries and Wages": 0.0,
    "Rent": 0.0,
    "Supplies": 0.0,
    "Utilities": 0.0
}
for category in deductions:
    deductions[category] = st.number_input(f"{category} ($)", min_value=0.0, format="%.2f", help=f"Enter total amount spent on {category.lower()}.")

total_deductions = sum(deductions.values())
st.write(f"**Total Deductions:** ${total_deductions:,.2f}")

st.header("Tax Liability and Savings")

taxable_income = max(annual_income - total_deductions, 0)
estimated_tax_liability = (taxable_income * (tax_rate / 100)) - other_tax_credits
estimated_tax_liability = max(estimated_tax_liability, 0)  # Ensure no negative tax liability

st.subheader("Results")

st.write(f"**Taxable Income after Deductions:** ${taxable_income:,.2f}")
st.write(f"**Estimated Tax Liability:** ${estimated_tax_liability:,.2f}")
if total_deductions > 0:
    savings_from_deductions = annual_income * (tax_rate / 100) - estimated_tax_liability
    st.write(f"**Potential Tax Savings from Deductions:** ${savings_from_deductions:,.2f}")
else:
    st.write("No deductions entered; add deductible expenses to estimate potential tax savings.")

st.subheader("Tax Savings Breakdown by Category")
category_contribution = {category: deductions[category] * (tax_rate / 100) for category in deductions}

category_data = list(category_contribution.values())
category_labels = list(category_contribution.keys())
category_data.sort(reverse=True)
category_labels = [x for _, x in sorted(zip(category_data, category_labels), reverse=True)]

# Plot the tax savings breakdown
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(category_labels, [category_contribution[category] for category in category_labels], color="skyblue")
ax.set_xlabel("Tax Savings ($)")
ax.set_title("Contribution of Each Deduction Category to Tax Savings")
st.pyplot(fig)

# Tax Bracket Calculation (Optional)
st.header("Tax Bracket Calculator (Optional)")

# User can opt for a progressive tax bracket calculator
apply_tax_bracket = st.checkbox("Apply Progressive Tax Brackets")
if apply_tax_bracket:
    st.write("**Progressive Tax Bracket Estimation**")
    brackets = [(0, 9950, 0.10), (9950, 40525, 0.12), (40525, 86375, 0.22), (86375, 164925, 0.24), (164925, 209425, 0.32), (209425, 523600, 0.35), (523600, np.inf, 0.37)]

    def calculate_bracket_tax(income):
        tax = 0
        for lower, upper, rate in brackets:
            if income > lower:
                taxable = min(upper, income) - lower
                tax += taxable * rate
            else:
                break
        return tax

    # Estimate tax using progressive brackets
    progressive_tax = calculate_bracket_tax(taxable_income)
    st.write(f"**Estimated Tax with Progressive Tax Brackets:** ${progressive_tax:,.2f}")

# Summary Section
st.markdown(
    """
    ### Summary
    This tool helps small business owners estimate their tax liabilities while considering deductible expenses and tax credits. By providing a breakdown of deductions and an optional progressive tax bracket estimator, businesses can gain better insights into potential tax savings. Remember to consult a tax professional to ensure accuracy for your specific situation.
    """
)
