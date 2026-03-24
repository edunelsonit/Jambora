import os
import sqlite3
import openai
from dotenv import load_dotenv

load_dotenv()

# Configuration
CORE_SUBJECTS = ["Mathematics", "English Language", "Physics", "Biology"]
DB_NAME = "jambora.db"
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_db():
    return sqlite3.connect(DB_NAME)

def seed_subjects():
    """Initializes the four core JAMB subjects."""
    with get_db() as conn:
        for sub in CORE_SUBJECTS:
            conn.execute("INSERT OR IGNORE INTO subjects (name) VALUES (?)", (sub,))
        conn.commit()
    print("✅ Subjects initialized.")

def fetch_top_topics(subject_name):
    """Uses AI to list the 15 most frequent JAMB topics for a subject."""
    print(f"🤖 Brainstorming topics for {subject_name}...")
    prompt = f"List exactly 15 essential exam topics for the JAMB {subject_name} syllabus. Return ONLY a comma-separated list of strings."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    topics_text = response.choices[0].message.content
    return [t.strip() for t in topics_text.split(',')]

def populate_topics():
    """Fetches and saves topics for each subject."""
    with get_db() as conn:
        subjects = conn.execute("SELECT id, name FROM subjects").fetchall()
        
        for sub_id, sub_name in subjects:
            topics = fetch_top_topics(sub_name)
            for topic_title in topics:
                conn.execute(
                    "INSERT INTO topics (subject_id, title) VALUES (?, ?)", 
                    (sub_id, topic_title)
                )
        conn.commit()
    print("🚀 Database successfully seeded with JAMB topics!")

if __name__ == "__main__":
    seed_subjects()
    populate_topics()