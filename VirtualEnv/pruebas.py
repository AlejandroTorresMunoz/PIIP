import sqlite3
import bcrypt

PATH_DDBB = "./DDBB/PIIP_DDBB.db" # Path where the database is located

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

        return True
    except:
        return False
    
def check_user(email : str, password : str) -> bool:
    """Function to check if an email and password are already registered"""
    try:
        conn = sqlite3.connect(PATH_DDBB)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT PASSWORD FROM Users WHERE EMAIL = ?
                       ''', (email,))
        
        result = cursor.fetchall()

        print(result)


        return True
    except:
        return False


check_user(email = "pip@gmail.com", password = "1234")