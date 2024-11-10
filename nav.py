import streamlit as st

class Nav:
    def __init__(self,pages):
        pg = st.navigation(pages)
        pg.run()
        

        