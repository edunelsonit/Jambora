import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import get_db_connection

def show():
    st.title("📊 Your Learning Progress")
    user_id = st.session_state.user['id']
    
    with get_db_connection() as conn:
        # Performance over time
        results_df = pd.read_sql(f"""
            SELECT r.score, r.total, r.timestamp, s.name as subject 
            FROM results r 
            JOIN subjects s ON r.subject_id = s.id 
            WHERE r.user_id = {user_id}
        """, conn)

    if not results_df.empty:
        results_df['percent'] = (results_df['score'] / results_df['total']) * 100
        
        # 1. Subject Mastery Chart
        fig = px.bar(results_df.groupby('subject')['percent'].mean().reset_index(), 
                     x='subject', y='percent', title="Average Score by Subject",
                     labels={'percent': 'Mastery %'})
        st.plotly_chart(fig)
        
        # 2. Recent Activity
        st.subheader("Recent Quizzes")
        st.dataframe(results_df[['timestamp', 'subject', 'score', 'total']].tail(10))
    else:
        st.warning("No data yet. Head over to Practice Mode to start learning!")