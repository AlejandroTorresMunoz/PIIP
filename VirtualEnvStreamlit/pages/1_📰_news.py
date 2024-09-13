import streamlit as st
import PyPDF2
import os
from src.news_files import load_pdf_files


# Configuration of the page
st.set_page_config(page_title="News", page_icon=":newspaper:")
if 'user_logged' in st.session_state and st.session_state.user_logged == True:
    st.sidebar.write(f"User : {st.session_state.email}")
else:
    st.sidebar.write("Please. log in.")



pdf_files = load_pdf_files()

with st.container():
    st.title("News and Articles")
    col_news, col_articles = st.columns(2)
    with col_news:
        st.title("News")
    with col_articles:
        st.title("Articles")
        # Read the PDF files
        for pdf_path in pdf_files:
            # Get the name of the file
            pdf_name = os.path.basename(pdf_path)
            with st.expander(f"{pdf_name}"):
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_bytes = pdf_file.read()
                    st.download_button(label="Download article", data=pdf_bytes, file_name=pdf_name)
                
                # Display PDF
                st.write(f"Preview of {pdf_name}")
                # st.pd

