import streamlit as st
from src.user_files import login, signup, save_user_config, load_user_config, save_user_preferences, load_user_preferences
from src.market_files import load_data_market, load_companies

# Data of the different markets
MARKETS = ['Ibex35',
           'Nasdaq']

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
        # Container de pruebas
        st.title("Interests")
        with st.container():
            st.header("Indexes")
        with st.container():
            st.header("Companies")
            # Display a selector to show markets to be displayed
            selected_option = st.selectbox("Select a market : ", MARKETS)
            # Get the companies contained in the selected option
            df_original = load_companies(selected_option)
            # Get the data of all the companies available
            
            # Load the selected options of the user
            list_companies_interest = load_user_preferences(selected_option)
            if list_companies_interest is None:
                # In the case the user has not saved any configuration for the selected market yet
                df_original['Interested'] = False
            else:
                df_original['Interested'] = df_original['name'].isin(list_companies_interest)
            # Dataframe with the data of the companies
            df_tickers_preferences = st.data_editor(data=df_original,
                    use_container_width=True,
                    hide_index=True,
                    )
            st.button("Save", key="users_preferences_button", on_click=lambda : save_user_preferences(df_tickers_preferences, selected_option))
