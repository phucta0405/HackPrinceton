import pytesseract
from PIL import Image
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import re
import streamlit as st
from pdf2image import convert_from_path

# Sample data for model training (replace with real data in production)
sample_data = pd.DataFrame({
    'wages': [50000, 60000, 75000, 85000],
    'federal_tax_withheld': [5000, 6000, 7500, 8500],
    'social_security_wages': [50000, 60000, 75000, 85000],
    'medicare_wages': [50000, 60000, 75000, 85000],
    'total_income': [150000, 180000, 225000, 255000],
    'tax_liability': [8000, 9000, 11000, 12000]
})

# Train the tax prediction model
X = sample_data[['wages', 'federal_tax_withheld', 'social_security_wages', 'medicare_wages', 'total_income']]
y = sample_data['tax_liability']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# OCR extraction with added detail and error handling for PDF files
def extract_w2_data_from_pdf(pdf_path):
    try:
        # Convert PDF to images (one image per page)
        images = convert_from_path(pdf_path)
        
        # For simplicity, assume W-2 info is on the first page
        text = pytesseract.image_to_string(images[0])
        
        # Regular expressions to extract W-2 fields
        w2_data = {
            'wages': re.search(r'Wages.*\$(\d{1,3}(,\d{3})*(\.\d{2})?)', text),
            'federal_tax_withheld': re.search(r'Federal.*\$(\d{1,3}(,\d{3})*(\.\d{2})?)', text),
            'social_security_wages': re.search(r'Social Security Wages.*\$(\d{1,3}(,\d{3})*(\.\d{2})?)', text),
            'medicare_wages': re.search(r'Medicare Wages.*\$(\d{1,3}(,\d{3})*(\.\d{2})?)', text)
        }
        
        # Parse extracted text into a numerical format
        parsed_data = {
            k: float(v.group(1).replace(',', '')) if v else 0.0 for k, v in w2_data.items()
        }
        
        # Check if any key data is missing
        if not all(parsed_data.values()):
            st.warning("Warning: Some fields could not be extracted. Verify the uploaded image.")
        
        return parsed_data
    except Exception as e:
        st.error(f"Error extracting data from W-2: {e}")
        return None

# Prepare extracted data for prediction
def prepare_data(w2_data):
    df = pd.DataFrame([w2_data])
    df['total_income'] = df['wages'] + df['social_security_wages'] + df['medicare_wages']
    return df[['wages', 'federal_tax_withheld', 'social_security_wages', 'medicare_wages', 'total_income']]

# Predict tax liability using model and optionally adjust based on user input
def predict_tax_liability(data, model):
    input_data = prepare_data(data)
    return model.predict(input_data)[0]

# Streamlit app setup
st.title("Tax Filing Assistance with W-2 Form")
st.write("Upload your W-2 to calculate estimated tax liability and adjust for filing specifics.")

# File upload
uploaded_file = st.file_uploader("Upload your W-2 form (PDF format)", type="pdf")
if uploaded_file is not None:
    # Save the uploaded file temporarily
    with open("temp_w2.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract data from W-2 and display
    extracted_data = extract_w2_data_from_pdf("temp_w2.pdf")
    if extracted_data:
        st.subheader("Extracted W-2 Data")
        st.write(extracted_data)
        
        # Allow user to adjust extracted data
        wages = st.number_input("Wages", value=extracted_data['wages'])
        federal_tax_withheld = st.number_input("Federal Tax Withheld", value=extracted_data['federal_tax_withheld'])
        social_security_wages = st.number_input("Social Security Wages", value=extracted_data['social_security_wages'])
        medicare_wages = st.number_input("Medicare Wages", value=extracted_data['medicare_wages'])
        
        # Update extracted data with any manual adjustments
        adjusted_data = {
            'wages': wages,
            'federal_tax_withheld': federal_tax_withheld,
            'social_security_wages': social_security_wages,
            'medicare_wages': medicare_wages
        }
        
        # Add filing details
        st.subheader("Additional Tax Details")
        dependents = st.number_input("Number of Dependents", min_value=0, step=1)
        filing_status = st.selectbox("Filing Status", ["Single", "Married Filing Jointly", "Head of Household"])
        
        # Simulate filing status adjustment
        filing_adjustment = 0.9 if filing_status == "Married Filing Jointly" else 1.1 if filing_status == "Head of Household" else 1.0
        dependents_adjustment = max(1 - (dependents * 0.02), 0.8)  # Dependents decrease tax by up to 20%
        
        # Calculate predicted tax liability
        base_tax = predict_tax_liability(adjusted_data, model)
        adjusted_tax_liability = base_tax * filing_adjustment * dependents_adjustment
        
        # Display prediction results
        st.subheader("Tax Prediction Results")
        st.write("**Base Tax Liability**: $", round(base_tax, 2))
        st.write("**Adjusted Tax Liability**: $", round(adjusted_tax_liability, 2))
        st.info("Adjusted tax liability accounts for filing status and dependents.")

    else:
        st.error("Failed to extract data. Please ensure the PDF is clear and in a readable format.")
