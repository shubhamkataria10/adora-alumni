import streamlit as st
from utils.auth import authenticate_student, register_student
from utils.database import get_student_by_email

def show_signup_page():
    """Display student signup page"""
    
    st.title("🎓 Student Registration")
    
    # Back button
    if st.button("← Back to Login"):
        st.session_state.page = 'student_login'
        st.rerun()
    
    st.markdown("---")
    
    with st.form("student_signup_form"):
        st.markdown("#### Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            email = st.text_input("Email Address *", placeholder="Enter your email")
            phone = st.text_input("Phone Number", placeholder="Enter your phone number")
        
        with col2:
            batch = st.number_input("Batch Year *", min_value=1950, max_value=2030, value=2020)
            branch = st.selectbox("Branch *", 
                                ["Computer Science", "Electronics", "Mechanical", "Civil", 
                                 "Electrical", "Chemical", "Information Technology", "Other"])
            linkedin = st.text_input("LinkedIn Profile", placeholder="LinkedIn URL (optional)")
        
        st.markdown("#### Professional Information")
        
        col3, col4 = st.columns(2)
        
        with col3:
            current_company = st.text_input("Current Company", placeholder="Enter current company")
            designation = st.text_input("Designation", placeholder="Enter your designation")
        
        with col4:
            working_status = st.selectbox("Working Status", 
                                        ["Employed", "Self-Employed", "Unemployed", "Student", "Other"])
            location = st.text_input("Current Location", placeholder="Enter current city/location")
        
        submitted = st.form_submit_button("Register", type="primary", use_container_width=True)
        
        if submitted:
            if not all([name, email, batch, branch]):
                st.error("Please fill in all required fields marked with *")
            else:
                student_data = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'batch': batch,
                    'branch': branch,
                    'linkedin': linkedin,
                    'current_company': current_company,
                    'designation': designation,
                    'working_status': working_status,
                    'location': location
                }
                
                if register_student(student_data):
                    st.session_state.page = 'student_login'
                    st.rerun()

def show_login_page():
    """Display student login page"""
    
    st.title("👨‍🎓 Student Login")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("student_login_form"):
            st.markdown("#### Login to your account")
            
            email = st.text_input("Email Address", placeholder="Enter your registered email")
            name = st.text_input("Full Name", placeholder="Enter your full name")
            
            col_batch, col_branch = st.columns(2)
            with col_batch:
                batch = st.number_input("Batch Year", min_value=1950, max_value=2030, value=2020)
            with col_branch:
                branch = st.selectbox("Branch", 
                                    ["Computer Science", "Electronics", "Mechanical", "Civil", 
                                     "Electrical", "Chemical", "Information Technology", "Other"])
            
            submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submitted:
                if not all([email, name, batch, branch]):
                    st.error("Please fill in all fields")
                else:
                    # Check if student exists
                    student = get_student_by_email(email)
                    if student:
                        # Verify basic info matches
                        if (student.get('name', '').lower() == name.lower() and 
                            student.get('batch') == batch and 
                            student.get('branch') == branch):
                            
                            st.session_state.user_data = student
                            st.session_state.page = 'student_dashboard'
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Student information doesn't match our records")
                    else:
                        st.error("Student not found. Please sign up first.")
        
        # Signup link
        st.markdown("---")
        if st.button("Don't have an account? Sign Up", use_container_width=True):
            st.session_state.page = 'student_signup'
            st.rerun()
