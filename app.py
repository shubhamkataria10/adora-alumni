import streamlit as st
import os
from firebase_config import initialize_firebase
from utils.database import init_database
from pages.landing import show_landing_page
from pages.student_auth import show_signup_page, show_login_page  
from pages.student_dashboard import show_dashboard
from pages.admin_auth import show_admin_login
from pages.admin_dashboard import show_admin_dashboard

# Initialize Firebase and Database
initialize_firebase()
init_database()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

def main():
    st.set_page_config(
        page_title="Alumni Connect",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Navigation logic based on session state
    if st.session_state.page == 'landing':
        show_landing_page()
    elif st.session_state.page == 'student_signup':
        show_signup_page()
    elif st.session_state.page == 'student_login':
        show_login_page()
    elif st.session_state.page == 'student_dashboard':
        show_dashboard()
    elif st.session_state.page == 'admin_login':
        show_admin_login()
    elif st.session_state.page == 'admin_dashboard':
        show_admin_dashboard()

if __name__ == "__main__":
    main()
