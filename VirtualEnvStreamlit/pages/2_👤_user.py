import streamlit as st
from src.user_files import login, signup, save_user_config

# Configuration of the page 
st.set_page_config(page_title="User", page_icon=":bust_in_silhouette:")
if 'user_logged' in st.session_state and st.session_state.user_logged == True:
    st.sidebar.write(f"User : {st.session_state.email}")
else:
    st.sidebar.write("Please. log in.")

if 'user_logged' not in st.session_state:
    # The user is not logged yet
    with st.container():
        # Log In section
        st.title("Log In")
        email_user= st.text_input(label="Email", type="default", key="login_email")
        password_user= st.text_input(label="Password", type="password", key="login_password")
        st.session_state.email_login = email_user
        st.session_state.password_login = password_user
        result = st.button(label="Log In", on_click=login)
    with st.container():
        # Sign Up section
        st.title("Sign Up")
        email_user = st.text_input(label="Email", type="default", key="signup_email")
        password_user = st.text_input(label="Password", type="password", key="signup_password")
        st.session_state.email_signup = email_user
        st.session_state.password_signup = password_user
        st.button(label="Sign Up", on_click=signup)
elif 'user_logged' in st.session_state and st.session_state.user_logged == True:
    # The user is already logged
    with st.container():
        # Configuration of the notification
        st.title("Notifications")
        st.subheader("Configuration of the notifications to be received.")
        st.session_state.receive_email_notifications = st.checkbox("Receive notifications through email.")
        st.session_state.periodicity_notifications = st.radio("Periodicity of the notifications", options=["Daily", "Weekly", "Monthly", "Never"], index=0)
        st.button("Save", on_click=save_user_config)

    with st.container():
        st.title("Interests")
