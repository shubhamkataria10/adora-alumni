import streamlit as st
from utils.auth import authenticate_admin

def show_admin_login():
    """Display admin login page"""
    
    st.title("👨‍💼 Admin Login")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("admin_login_form"):
            st.markdown("#### Admin Access")
            
            username = st.text_input("Username", placeholder="Enter admin username")
            password = st.text_input("Password", type="password", placeholder="Enter admin password")
            
            submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    if authenticate_admin(username, password):
                        st.session_state.admin_authenticated = True
                        st.session_state.page = 'admin_dashboard'
                        st.success("Admin login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
        
        # Default credentials info
        st.markdown("---")
        st.info("Default credentials: Username: admin, Password: admin")
        st.caption("This environment starts a mock API server at http://127.0.0.1:5055")
