import streamlit as st
from database.crud import get_subjects, get_topics, add_question
from services.ai_generator import generate_exam_content

def show():
    st.header("🛡️ JAMBORA Content Command")
    
    # 1. Select Context
    subs = get_subjects()
    selected_sub = st.selectbox("Select Subject", subs, format_func=lambda x: x['name'])
    
    if selected_sub:
        topics = get_topics(selected_sub['id'])
        selected_topic = st.selectbox("Select Topic to Populate", topics, format_func=lambda x: x['title'])
        
        # 2. Trigger Generation
        num_q = st.slider("Questions to generate", 5, 20, 5)
        
        if st.button(f"Generate Questions for {selected_topic['title']}"):
            with st.spinner("AI is analyzing the syllabus and writing questions..."):
                try:
                    raw_questions = generate_exam_content(selected_sub['name'], selected_topic['title'])
                    
                    for q in raw_questions:
                        add_question(selected_topic['id'], q)
                        
                    st.success(f"Added {len(raw_questions)} questions to {selected_topic['title']}!")
                except Exception as e:
                    st.error(f"Failed to generate: {e}")

    st.divider()
    st.info("Note: Ensure your OpenAI API key has sufficient quota.")