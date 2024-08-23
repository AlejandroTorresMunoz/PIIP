import streamlit as st
import psycopg2
from psycopg2 import sql
import pandas as pd
MARKETS = {'Ibex35' : 'ibex35data',
           'Nasdaq' : 'nasdaqdata'}

def load_data_market(selected_database : str) ->pd.DataFrame:
    """ TO CHECK : Method to load the database from a market"""
    try:
        db_config = st.secrets["connections"]["postgresql"]

        conn = psycopg2.connect(host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user= db_config['username'],
            password= db_config['password'])
        
        query = f"SELECT * FROM {selected_database};"
        result = conn.query(query)
        return result
    except Exception as e:
        st.error(f"Internal error : {e}")

def load_companies(selected_market : str)->pd.DataFrame:
    """Method to load the available companies"""
    # Connect to DDBB
    conn = st.connection("postgresql", type="sql")
    # Check if user exists
    query = f"SELECT * FROM {MARKETS[selected_market]};"
    result = conn.query(query)
    return result
        
    