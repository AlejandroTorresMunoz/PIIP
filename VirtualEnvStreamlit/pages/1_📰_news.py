import streamlit as st

# Configuration of the page
st.set_page_config(page_title="News", page_icon=":newspaper:")
if 'user_logged' in st.session_state and st.session_state.user_logged == True:
    st.sidebar.write(f"User : {st.session_state.email}")
else:
    st.sidebar.write("Please. log in.")

with st.container():
    st.title("Latest News")