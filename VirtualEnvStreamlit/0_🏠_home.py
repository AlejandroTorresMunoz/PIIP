"""
Main file of the project.
"""

import streamlit as st
import pandas as pd

# Configuration of the page 
st.set_page_config(page_title="Home", page_icon=":house:")

with st.expander(label="Quiénes Somos", icon="🧐"):
    st.write("Texto de explicación")

with st.expander(label="Objetivos", icon="🎯"):
    st.write("Texto de explicación")

with st.expander(label="Cómo Funciona", icon="❓"):
    st.write("Texto de explicación")

with st.expander(label="Testimonios", icon="🗞️"):
    st.write("Texto de explicación")