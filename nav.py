import streamlit as st

class Nav:
    def __init__(self,pages):
        self.pages = st.navigation(pages)
        self.pages.run()
        

        