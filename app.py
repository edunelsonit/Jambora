import streamlit as st
from database.db import init_db
from database.crud import sync_user
from pages import practice, dashboard, admin_panel # assume modules created

init_db()

def main():
    st.sidebar.title("JAMBORA AI")
    
    # Simple Mock Auth for Demo (Replace with Auth0 logic)
    if 'user' not in st.session_state:
        email = st.text_input("Enter Email to 'Login'")
        if st.button("Login"):
            # In production, this data comes from Auth0
            user_data = {"email": email, "nickname": email.split('@')[0], "picture": ""}
            st.session_state.user = sync_user(user_data)
            st.rerun()
    else:
        page = st.sidebar.radio("Go to", ["Dashboard", "Practice", "Admin"])
        
        if page == "Practice":
            practice.show()
        elif page == "Admin":
            admin_panel.show()
        else:
            st.write(f"# Hello, {st.session_state.user['name']}!")
            st.write("Welcome to your JAMB dashboard.")

        if st.sidebar.button("Logout"):
            del st.session_state.user
            st.rerun()

if __name__ == "__main__":
    main()