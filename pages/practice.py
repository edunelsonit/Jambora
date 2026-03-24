import streamlit as st
from database.crud import get_subjects, get_topics, get_questions, save_score
from services.tts import get_audio_html

def show():
    st.title("📝 Practice Center")
    subs = get_subjects()
    sub = st.selectbox("Subject", subs, format_func=lambda x: x['name'])
    
    if sub:
        tops = get_topics(sub['id'])
        top = st.selectbox("Topic", tops, format_func=lambda x: x['title'])
        
        if st.button("Start Quiz"):
            st.session_state.quiz = get_questions(top['id'])
            st.session_state.q_idx = 0
            st.session_state.score = 0
            st.rerun()

    if 'quiz' in st.session_state:
        q = st.session_state.quiz[st.session_state.q_idx]
        st.write(f"### {q['question']}")
        
        if st.button("🔊 Listen"):
            st.components.v1.html(get_audio_html(q['question']), height=0)
            
        choice = st.radio("Options", [q['a'], q['b'], q['c'], q['d']])
        
        if st.button("Submit Answer"):
            is_correct = choice.lower() == q[q['answer'].lower()].lower()
            if is_correct:
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(f"Incorrect. Answer was {q['answer'].upper()}")
            st.info(f"Why? {q['explanation']}")
            
            if st.session_state.q_idx + 1 < len(st.session_state.quiz):
                st.session_state.q_idx += 1
                st.button("Next")
            else:
                save_score(st.session_state.user['id'], sub['id'], st.session_state.score, len(st.session_state.quiz))
                st.write("Quiz Finished!")
                if st.button("Exit"):
                    del st.session_state.quiz
                    st.rerun()