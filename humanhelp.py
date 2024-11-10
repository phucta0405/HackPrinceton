import streamlit as st

def support():
    st.title("Request A Financial Assistant Help")
    st.markdown(
        """
        **Need assistance?**  
        If our AI chatbot couldn't help you, our human support team is here to assist you. Please fill out the form below, and someone from our team will get in touch with you as soon as possible.
        """
    )
    with st.form(key="support_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        message = st.text_area("Message", help="Describe the issue you need assistance with.")
        submit_button = st.form_submit_button("Submit Request")

        if submit_button:
            if name and email and message:
                st.success("Thank you for your request! We will get back to you soon.")
            else:
                st.error("Please fill out all fields.")

# Set page configuration
# st.set_page_config(page_title="Request Human Help", layout="centered")

# Call the support function when this page is selected
support()
