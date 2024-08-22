"""
Main file of the project.
"""

import streamlit as st
import pandas as pd
from streamlit_extras.bottom_container import bottom

# Configuration of the page 
st.set_page_config(page_title="Home", page_icon=":house:")
if 'user_logged' in st.session_state and st.session_state.user_logged == True:
    st.sidebar.write(f"User : {st.session_state.email}")
else:
    st.sidebar.write("Please. log in.")


with st.expander(label="Quiénes Somos", icon="🧐"):
    st.write("Texto de explicación")

with st.expander(label="Objetivos", icon="🎯"):
    st.write("Texto de explicación")

with st.expander(label="Cómo Funciona", icon="❓"):
    st.write("Texto de explicación")

with st.expander(label="Testimonios", icon="🗞️"):
    st.write("Texto de explicación")

