import streamlit as st
import hashlib
from utils.database import get_student_by_email, create_student, get_admin_credentials
import streamlit as st

# Parent auth placeholder using in-memory storage in session
def authenticate_parent(email: str, child_email: str):
    parent = st.session_state.get('parent_users', {}).get(email)
    child = get_student_by_email(child_email)
    if child:
        return { 'email': email, 'child_email': child_email }
    return None

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_student(email, name, batch, branch):
    """Authenticate student with basic info"""
    try:
        student = get_student_by_email(email)
        if student:
            # Update student info if exists
            student_data = {
                'name': name,
                'email': email,
                'batch': batch,
                'branch': branch
            }
            return student_data
        else:
            st.error("Student not found. Please sign up first.")
            return None
    except Exception as e:
        st.error(f"Authentication failed: {e}")
        return None

def register_student(student_data):
    """Register new student"""
    try:
        # Check if student already exists
        existing_student = get_student_by_email(student_data['email'])
        if existing_student:
            st.error("Student with this email already exists!")
            return False
        
        # Create new student
        success = create_student(student_data)
        if success:
            st.success("Registration successful! You can now login.")
            return True
        else:
            st.error("Registration failed. Please try again.")
            return False
    except Exception as e:
        st.error(f"Registration failed: {e}")
        return False

def authenticate_admin(username, password):
    """Authenticate admin user"""
    try:
        admin_creds = get_admin_credentials()
        hashed_password = hash_password(password)
        
        if admin_creds and admin_creds.get('username') == username and admin_creds.get('password') == hashed_password:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Admin authentication failed: {e}")
        return False

def logout():
    """Clear session state for logout"""
    st.session_state.user_role = None
    st.session_state.user_data = None
    st.session_state.admin_authenticated = False
    st.session_state.page = 'landing'
    st.rerun()
