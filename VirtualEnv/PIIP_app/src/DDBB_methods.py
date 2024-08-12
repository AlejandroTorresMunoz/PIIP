import sqlite3
import bcrypt

PATH_DDBB = "../DDBB/PIIP_DDBB.db" # Path where the database is located

def hash_password(password : str):
    """Function to hash a given password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def add_user(email : str, password : str) -> bool:
    """Function to add a new user to the Users table"""
    try:
        conn = sqlite3.connect(PATH_DDBB)
        cursor = conn.cursor()
             
        password_hash = hash_password(password)
        
        cursor.execute('''
        INSERT INTO Users (EMAIL, PASSWORD)
        VALUES (?, ?)
        ''', (email, password_hash))
        
        conn.commit()
        conn.close()

        print("Usuario añadido")

        return True
    except:
        return False
    
def check_user(email: str, password: str) -> tuple[bool, bool]:
    """Function to check if an email and password are already registered"""
    try:
        conn = sqlite3.connect(PATH_DDBB)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT PASSWORD FROM Users WHERE EMAIL = ?
                       ''', (email,))
                
        result = cursor.fetchone()  # Utilizamos fetchone ya que esperamos solo una fila
        

        if result is None:
            # Email not registered
            return (False, False)
        else:
            stored_password = result[0]
            check_password = bcrypt.checkpw(password.encode('utf-8'), stored_password)
            if check_password:
                # Correct password
                return (True, True)
            else:
                # Wrong password
                return (True, False)
    except Exception as e:
        print(f"Error: {e}")
        return (False, False)
    finally:
        cursor.close()
        conn.close()

