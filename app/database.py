import sqlite3
import os

DATABASE_PATH=os.path.join(os.path.dirname(__file__), 'notes.db')


def get_connection(): 
  
    db=sqlite3.connect(DATABASE_PATH)
    db.row_factory=sqlite3.Row
    return db


def init_database():
    
    db=get_connection()
    cursor=db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            totp_secret BLOB NOT NULL,
            totp_iv BLOB NOT NULL,
            totp_salt BLOB NOT NULL,
            failed_attempts INTEGER DEFAULT 0,
            locked_until REAL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    db.commit()
    db.close()




def create_user(username, password_hash, totp_secret, totp_iv, totp_salt):
    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (username, password_hash, totp_secret, totp_iv, totp_salt) VALUES (?, ?, ?, ?, ?)',
            (username, password_hash, totp_secret, totp_iv, totp_salt)
        )
        db.commit()
        user_id=cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        db.close()


def get_user_by_username(username):
    db=get_connection()
    cursor=db.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user=cursor.fetchone()
    db.close()
    return user


##def get_user_by_id(user_id):
  ##cursor = db.cursor()
  ##  cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
  ##  user = cursor.fetchone()
  ##  db.close()
  ##  return user

def update_failed_attempts(username, attempts, locked_until=0):
    db=get_connection()
    cursor=db.cursor()
    cursor.execute(
        'UPDATE users SET failed_attempts = ?, locked_until = ? WHERE username = ?',
        (attempts, locked_until, username)
    )

    db.commit()
    db.close()


def reset_failed_attempts(username):
    update_failed_attempts(username, 0, 0)



def create_note(user_id, content):
    if not content.strip(): #Pusty
        return None

    db=get_connection()
    cursor=db.cursor()

    cursor.execute(
        'INSERT INTO notes (user_id, content) VALUES (?, ?)',
        (user_id, content)
    )

    db.commit()
    note_id=cursor.lastrowid
    db.close()

    return note_id

def get_note_by_id(note_id, user_id):
    db=get_connection()
    cursor=db.cursor()
    
    cursor.execute(
        'SELECT id, content FROM notes WHERE id=? AND user_id=?',
        (note_id, user_id)
    
    )
    note=cursor.fetchone()
    db.close()
    return note




def delete_note(note_id, user_id):
    
    db=get_connection()
    cursor=db.cursor()

    cursor.execute(
        'DELETE FROM notes WHERE id = ? AND user_id = ?',
        (note_id, user_id)
    )

    deleted=cursor.rowcount > 0
    db.commit()
    db.close()

    return deleted


def get_all_notes(user_id):
    db=get_connection()
    cursor=db.cursor()

    cursor.execute(
        'SELECT id, content FROM notes WHERE user_id=?',(user_id,)
    )
    notes=cursor.fetchall()
    db.close()
    return notes



if __name__ == '__main__':
    init_database()
