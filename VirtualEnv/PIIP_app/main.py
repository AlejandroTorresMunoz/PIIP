import streamsync as ss
import sqlite3 
from PIIP_app.src.DDBB_methods import add_user, check_user

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
    else:
        USER_LOGGED = False

    
# Initialise the state

# "_my_private_element" won't be serialised or sent to the frontend,
# because it starts with an underscore

initial_state = ss.init_state({
    "my_app": {
        "title": "PIIP_app"
    },
    "_my_private_element": 1337,
    "email_login" : "",
    "email_signup" : "",
    "password_login" : "",
    "password_signup" : "",
    "login_signup_visibility" : True,
    "user_visibility" : False
})

