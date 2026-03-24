from .db import get_db_connection

def sync_user(user_info):
    with get_db_connection() as conn:
        conn.execute("""INSERT INTO users (email, name, picture) VALUES (?, ?, ?)
                        ON CONFLICT(email) DO UPDATE SET name=excluded.name""", 
                     (user_info['email'], user_info['nickname'], user_info['picture']))
        conn.commit()
        return conn.execute("SELECT * FROM users WHERE email=?", (user_info['email'],)).fetchone()

def get_subjects():
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM subjects").fetchall()

def get_topics(subject_id):
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM topics WHERE subject_id=?", (subject_id,)).fetchall()

def get_questions(topic_id):
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM questions WHERE topic_id=?", (topic_id,)).fetchall()

def save_score(user_id, subject_id, score, total):
    with get_db_connection() as conn:
        conn.execute("INSERT INTO results (user_id, subject_id, score, total) VALUES (?, ?, ?, ?)",
                     (user_id, subject_id, score, total))
        conn.commit()