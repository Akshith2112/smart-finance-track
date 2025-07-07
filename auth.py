from db import get_connection
import bcrypt

def load_users():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT username, password FROM users')
        rows = c.fetchall()
        return [{'username': row[0], 'password': row[1]} for row in rows]

def add_user(username, password):
    if not username or not password or len(username.strip()) < 3 or len(password) < 6:
        return False, "Username must be at least 3 chars and password at least 6 chars."
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM users WHERE username = ?', (username,))
        if c.fetchone():
            return False, "Username already exists."
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
        return True, "Account created successfully."

def verify_user(username, password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE username = ?', (username,))
        row = c.fetchone()
        if not row:
            return False
        hashed = row[0]
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False 