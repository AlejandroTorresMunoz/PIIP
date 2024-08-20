import streamlit as st
from src.user_files import login, signup

st.set_page_config(page_title="User", page_icon=":bust_in_silhouette:")

if 'UserLogged' not in st.session_state:
    # The user is not logged yet
    with st.container():
        # Log In section
        st.title("Log In")
        email_user= st.text_input(label="Email", type="default", key="login_email")
        password_user= st.text_input(label="Password", type="password", key="login_password")
        result = st.button(label="Log In", on_click=login)
    with st.container():
        # Sign Up section
        st.title("Sign Up")
        email_user = st.text_input(label="Email", type="default", key="signup_email")
        password_user = st.text_input(label="Password", type="password", key="signup_password")
        st.button(label="Sign Up", on_click=signup)
elif 'UserLogged' in st.session_state:
    # The user is already logged
    pass

