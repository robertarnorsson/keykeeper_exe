import os
import sqlite3

from constants import PROJECT_DIR

def connect_db(db):
    conn = sqlite3.connect(os.path.join(PROJECT_DIR, f'./database/{db}.db'))
    return conn

def connect_iuser_db(user_uuid, db):
    conn = sqlite3.connect(os.path.join(PROJECT_DIR, f'./database/{user_uuid}/data/{db}.db'))
    return conn

def make_users_table():
    conn = connect_db('users')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_uuid TEXT NOT NULL,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                slt TEXT NOT NULL,
                pep TEXT NOT NULL
            )
        ''')
    conn.commit()
    conn.close()

def create_iuser_database(user_uuid, database_name):
    # Connect to the database (creates it if it doesn't exist)
    conn = connect_iuser_db(user_uuid, database_name)
    cursor = conn.cursor()

    # Create the table
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                title TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                icon TEXT NOT NULL,
                lvl TEXT NOT NULL
            )
        ''')
    conn.commit()
    conn.close()
    print(f"Database '{database_name}' created successfully.")

def save_user(database_name, user_uuid, name, password, slt, pep):
    conn = connect_db(database_name)
    cursor = conn.cursor()
    # Insert a new user into the database
    cursor.execute('''
        INSERT INTO users (user_uuid, name, password, slt, pep)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_uuid, name, password, slt, pep,))
    conn.commit()
    conn.close()

def retrieve_users():
    conn = connect_db('users')
    cursor = conn.cursor()
    # Retrieve all users from the database
    try:
        cursor.execute('''
            SELECT * FROM users
        ''')
        users = cursor.fetchall()
        conn.close()
        return users
    except:
        conn.close()
        return []

def retrieve_user_by_name(name):
    conn = connect_db('users')
    cursor = conn.cursor()
    # Retrieve all users from the database
    try:
        cursor.execute('''
            SELECT * FROM users WHERE name = ?
        ''', (name,))
        users = cursor.fetchall()
        conn.close()
        if users:
            return users[0]
        else:
            return []
    except:
        conn.close()
        return []

def save_password(database_name, user_uuid, title, username, password, icon, lvl):
    conn = connect_iuser_db(user_uuid, database_name)
    cursor = conn.cursor()
    # Insert a new password under the specified filter for the user
    cursor.execute('''
        INSERT INTO users (title, username, password, icon, lvl)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, username, password, icon, lvl,))
    conn.commit()
    conn.close()

def retrieve_passwords(database_name, user_uuid):
    conn = connect_iuser_db(user_uuid, database_name)
    cursor = conn.cursor()
    # Retrieve all items from the table
    cursor.execute('''
        SELECT * FROM users
    ''')
    items = cursor.fetchall()
    conn.close()
    return items

def retrieve_password_by_title(database_name, user_uuid, title):
    # Connect to the database
    conn = connect_iuser_db(user_uuid, database_name)
    cursor = conn.cursor()

    # Retrieve the item by name
    cursor.execute('''
        SELECT * FROM users WHERE title = ?
    ''', (title,))
    item = cursor.fetchall()
    conn.close()

    if item:
        return item
    else:
        return None
    
def retrieve_lvl_by_title(database_name, user_uuid, title):
    # Connect to the database
    conn = connect_iuser_db(user_uuid, database_name)
    cursor = conn.cursor()

    # Retrieve the item by name
    cursor.execute('''
        SELECT lvl FROM users WHERE title = ?
    ''', (title,))
    item = cursor.fetchall()
    conn.close()

    if item:
        return item
    else:
        return None

def update_password_by_title(database_name, user_uuid, title, new_title, username, password, icon, lvl):
    conn = connect_iuser_db(user_uuid, database_name)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users SET title = ?, username = ?, password = ?, icon = ?, lvl = ? WHERE title = ?
    ''', (new_title, username, password, icon, lvl, title,))

    conn.commit()
    conn.close()

def delete_password_by_title(database_name, user_uuid, title):
    conn = connect_iuser_db(user_uuid, database_name)
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM users WHERE title = ?
    ''', (title,))

    conn.commit()
    conn.close()