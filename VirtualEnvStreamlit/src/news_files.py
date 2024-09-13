import os
import streamlit as st
import psycopg2
from psycopg2 import sql

# @st.cache_resource
def load_pdf_files():
    # Connect to database
    conn = st.connection("postgresql", type="sql")
    # Get dataframe with the active articles
    query = f"SELECT * FROM articles WHERE active = {True};"
    result = conn.query(query)
    return result
