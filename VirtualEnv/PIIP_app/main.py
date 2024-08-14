import writer as wf
import sqlite3 
import pandas as pd

from PIIP_app.src.DDBB_methods import add_user, check_user
from PIIP_app.src.DDBB_methods import save_tickers_user


# This is a placeholder to get you started or refresh your memory.
# Delete it or adapt it as necessary.
# Documentation is available at https://streamsync.cloud

# Shows in the log when the app starts

USER_LOGGED = False

def login(state):
    """Function to redirect to another URL."""
    
    (check_email, check_password) = check_user(email=state["email_login"], 
               password=state["password_login"])
    if check_email and check_password:
        # Correct login
        USER_LOGGED = True
        state['login_signup_visibility'] = False
        state['user_visibility'] = True

        # Change active page
        state.set_page("UserPage")
    else:
        USER_LOGGED = False
    

def signup(state):
    """Function to redirect to another URL."""
    check_signup = add_user(email=state["email_signup"],
             password=state["password_signup"])
    if check_signup:
        # Correct signup
        USER_LOGGED = True
        state['login_signup_visibility'] = False
        state['user_visibility'] = True

        # Change active page
        state.set_page("UserPage")
    else:
        USER_LOGGED = False

    
# Initialise the state

# "_my_private_element" won't be serialised or sent to the frontend,
# because it starts with an underscore

# Load data of tickers 
available_tickers_df = pd.read_csv("./data/TickersData.csv")
tickers_user = {value : value for value in available_tickers_df.index.tolist()}
print(tickers_user)
print(type(tickers_user))

initial_state = wf.init_state({
    "my_app": {
        "title": "PIIP_app"
    },
    "_my_private_element": 1337,
    "email_login" : "",
    "email_signup" : "",
    "password_login" : "",
    "password_signup" : "",
    "login_signup_visibility" : True,
    "user_visibility" : False,
    "UserPageVisibility" : False,
    "available_tickers_df" : available_tickers_df,
    # "tickers_user" : tickers_user
})



