import streamlit as st
import PyPDF2
import os
from src.news_files import refresh_articles_container


# Configuration of the page
st.set_page_config(page_title="News", page_icon=":newspaper:")
if 'user_logged' in st.session_state and st.session_state.user_logged == True:
    st.sidebar.write(f"User : {st.session_state.email}")
else:
    st.sidebar.write("Please. log in.")

with st.container():
    st.title("News and Articles")
    col_news, col_articles = st.columns(2)
    with col_news:
        st.title("News")
    # Create the container for the articles
    with col_articles:
        refresh_articles_container()

        
