import os
import streamlit as st
import psycopg2
from psycopg2 import sql
import pandas as pd
import PyPDF2

def refresh_articles_container():
    """Method to create the container with the active articles"""
    pdf_files = load_pdf_files()
    with st.container():
        st.title("Articles")
        # Read the PDF files
        for i in range(len(pdf_files)):
            article_name = pdf_files.iloc[i]['name'].split('.pdf')[0] # Get the name of the article
            article_path = pdf_files.iloc[i]['path'] # Get the path where the article is stored
            with st.expander(f"{article_name}"):
                with open(article_path, 'rb') as pdf_file:
                    # summary = get_summary_article(pdf_file) # Ge summary of the article
                    # st.write(summary)
                    pdf_bytes = pdf_file.read()
                    st.download_button(label="Download article", data=pdf_bytes, file_name=article_name)
# TODO : To be completed
def get_summary_article(pdf_file):
    """Method to get the first lines of an article"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    first_page = pdf_reader.pages[0].extract_text() # Get first page text
    cleaned_text = first_page.replace('\n', ' ') # Clean multiple spaces
    cleaned_text = ' '.join(cleaned_text.split())
    summary_lines = cleaned_text.split('\n')[0] # Get the first 5 lines of text
    summary = "\n".join(summary_lines)
    print(summary)
    return summary



def load_pdf_files() -> pd.DataFrame :
    """Method to get a dataframe with a list of the active articles"""
    # Connect to database
    conn = st.connection("postgresql", type="sql")
    # Get dataframe with the active articles
    query = f"SELECT * FROM articles WHERE active = {True};"
    result = conn.query(query)
    return result

def get_first_lines_pdf(pdf_file):
    pass
