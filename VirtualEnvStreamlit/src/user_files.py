import streamlit as st
import hashlib
import psycopg2
from psycopg2 import sql


def login():
    """Method to check if the credential for the login requested are correct"""
    try:
        # Connect to DDBB
        conn = st.connection("postgresql", type="sql")

        # Check if user existss
        query = f"SELECT * FROM users WHERE email = '{st.session_state.email_login}';"
        
        result = conn.query(query)
        if not result.empty:
            # Email registered
            input_password = hashlib.sha256(st.session_state.password_login.encode()).hexdigest()
            registered_password = result['password'].iloc[0]
            if input_password == registered_password:
                st.session_state.email = st.session_state.email_login
                st.session_state.pop('email_login')
                st.session_state.pop('password_login')
                st.session_state['user_logged'] = True
                st.success("Login done.")
        else:
            st.warning("Email not registered.")
    except Exception as e:
        st.error(f"Internal error : {e}")

def signup():
    """Method to sign up a new user"""
    
    try:
        # Connect to DDBB
        conn = st.connection("postgresql", type="sql")

        # Check if user exists
        query = f"SELECT * FROM users WHERE email = '{st.session_state.email_signup}';"
        result = conn.query(query)

        if not result.empty:
            st.warning("Email already registered.")
        else:
    
            db_config = st.secrets["connections"]["postgresql"]

            conn = psycopg2.connect(host=db_config['host'],
                      port=db_config['port'],
                      database=db_config['database'],
                      user= db_config['username'],
                      password= db_config['password'])

            cursor = conn.cursor()

            # Codificar la contraseña
            hashed_password = hashlib.sha256(st.session_state.password_signup.encode()).hexdigest()

            # Crear la consulta SQL
            insert_query = sql.SQL("""
                INSERT INTO users (email, password)
                VALUES (%s, %s);
            """)

            # Ejecutar la consulta
            cursor.execute(insert_query, (st.session_state.email_signup, hashed_password))

            # Confirmar los cambios
            conn.commit()
            st.session_state.email = st.session_state.email_signup
            st.session_state.pop('email_signup')
            st.session_state.pop('password_signup')
            st.success("Email and Password registereds")
            st.session_state['user_logged'] = True

    except Exception as e:
        st.error(f"Internal error : {e}")

def save_user_config():
    """Method to save th configuration of the user"""
    try:
        db_config = st.secrets["connections"]["postgresql"]
        conn = psycopg2.connect(host=db_config['host'],
                      port=db_config['port'],
                      database=db_config['database'],
                      user= db_config['username'],
                      password= db_config['password'])
        cursor = conn.cursor()

        query = f"UPDATE user_preferences SET receive_email_notifications = {st.session_state.receive_email_notifications}, periodicity_notifications = '{st.session_state.periodicity_notifications}' WHERE email = '{st.session_state.email}';"
        cursor.execute(query)
        conn.commit()
        st.success("Changes saved successfully!")
    
    except Exception as e:
        st.error(f"Internal error : {e}")
    pass
