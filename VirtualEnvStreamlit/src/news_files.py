"""
Methods to handle the news and articles page
"""
import os
import streamlit as st
import psycopg2
from psycopg2 import sql
import pandas as pd
import docx

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
                with open(article_path, 'rb') as docx_file:
                    summary = get_summary_article(docx_file)
                    st.write(summary)
                    docx_bytes = docx_file.read()
                    st.download_button(label="Download article", data=docx_bytes, file_name=article_name)

# TODO : To be completed
def get_summary_article(docx_file):
    """Method to get the first lines of an article"""
    doc = docx.Document(docx_file)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    first_paragraph = paragraphs[1] if paragraphs else ""
    return first_paragraph


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
