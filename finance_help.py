import streamlit as st
from model import *
st.title("Finacial Wellnes Calculator")

# Declare a form and call methods directly on the returned object

form = st.form(key='Info')
form.text_input(label="Number of expenses")

form.text_input(label='Monthly Income', key = '43rk[o4ekge]')
submit_button = form.form_submit_button(label='Submit')