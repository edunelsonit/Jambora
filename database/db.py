import sqlite3

def get_db_connection():
    conn = sqlite3.connect("jambora.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        # Users
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            picture TEXT,
            role TEXT DEFAULT 'student')''')
        
        # Subjects
        conn.execute('''CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL)''')

        # Topics
        conn.execute('''CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            FOREIGN KEY(subject_id) REFERENCES subjects(id))''')

        # Questions
        conn.execute('''CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            question TEXT, a TEXT, b TEXT, c TEXT, d TEXT, 
            answer TEXT, explanation TEXT,
            FOREIGN KEY(topic_id) REFERENCES topics(id))''')

        # Results
        conn.execute('''CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject_id INTEGER,
            score INTEGER, total INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id))''')
        conn.commit()