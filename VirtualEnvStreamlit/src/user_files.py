import streamlit as st


def login():
    """Method to check if the credential for the login requested are correct"""
    if ('email_user' in st.session_state) and ('password_user' in st.session_state):
        # Connect with the DDBB
        """
        conn = st.connection('PIIP_DDBB', type='sql')
        
        with conn.session as s:
            s.execute("SELECT * FROM Users")
        st.session_state.email_user
        st.session_state.password_user
        """
        pass

def signup():
    """Method to sign up a new user"""
    print("Dentro de la función de signup")
    # if ('email_user' in st.session_state) and ('password_user' in st.session_state):
        # Connect with the DDBB
    conn = st.connection('PIIP_DDBB', type='sql')
    print("Conexión establecida con la base de datos")
    with conn.session as s:
        # Users, EMAIL. PASSWORD
        df = s.query("SELECT * FROM Users")
        print(df)