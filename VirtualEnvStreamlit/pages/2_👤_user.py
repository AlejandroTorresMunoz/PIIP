import streamlit as st
from src.user_files import login, signup, save_user_config, load_user_config
from src.market_files import load_data_market, load_companies

# Data of the different marketss
markets = {'Ibex35' : 'Ibex35Data',
           'Nasdaq' : 'NasdaqData'}

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
    load_user_config()
    with st.container():
        # Configuration of the notification
        st.title("Notifications")
        st.subheader("Configuration of the notifications to be received.")
        st.session_state.receive_email_notifications = st.checkbox("Receive notifications through email.", 
                                                                   value = st.session_state.receive_email_notifications)

        st.session_state.periodicity_notifications = st.radio("Periodicity of the notifications", 
                                                              options=["Daily", "Weekly", "Monthly", "Never"], 
                                                              index=["Daily", "Weekly", "Monthly", "Never"].index(st.session_state.periodicity_notifications))
        st.button("Save", on_click=save_user_config)

    with st.container():
        st.title("Interests")
        with st.container():
            st.header("Indexes")
        with st.container():
            st.header("Companies")
            # Display selector to show markets to be displayed
            
            # Get the with the avalaible companies in the selected market
            df_original = load_companies()
            # Add the column of the mark box
            df_original['Interested'] = False
            # Dataframe with the data of the companies
            st.data_editor(data=df_original,
                        use_container_width=True,
                        hide_index=True,
                        )


