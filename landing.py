import streamlit as st

def show_landing_page():
    """Display the landing page with role selection"""
    
    st.title("🎓 Alumni Connect")
    st.markdown("### Welcome to Alumni Connect Platform")
    st.markdown("Connect with alumni, explore opportunities, and stay engaged with your alma mater.")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("#### Choose your role to continue:")
        
        # Student button
        if st.button("👨‍🎓 Student", use_container_width=True, type="primary"):
            st.session_state.user_role = 'student'
            st.session_state.page = 'student_login'
            st.rerun()
        
        st.markdown("")
        
        # Admin button
        if st.button("👨‍💼 Admin", use_container_width=True):
            st.session_state.user_role = 'admin'
            st.session_state.page = 'admin_login'
            st.rerun()
    
    st.markdown("---")
    
    # Information section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### For Students:")
        st.markdown("""
        - View alumni directory
        - Connect with alumni
        - Explore career opportunities
        - Stay updated with events
        """)
    
    with col2:
        st.markdown("#### For Admins:")
        st.markdown("""
        - Manage alumni database
        - Add and update alumni records
        - Schedule events
        - Monitor platform activity
        """)
