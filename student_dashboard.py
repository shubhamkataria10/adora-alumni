import streamlit as st
import pandas as pd
from utils.database import get_all_alumni, get_all_events
from utils.auth import logout

def show_dashboard():
    """Display student dashboard"""
    
    if not st.session_state.user_data:
        st.session_state.page = 'landing'
        st.rerun()
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"Welcome, {st.session_state.user_data.get('name', 'Student')}!")
    with col2:
        if st.button("Logout", type="secondary"):
            logout()
    
    st.markdown("---")
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["📋 Alumni Directory", "📅 Upcoming Events", "👤 My Profile"])
    
    with tab1:
        show_alumni_directory()
    
    with tab2:
        show_events()
    
    with tab3:
        show_profile()

def show_alumni_directory():
    """Display alumni directory with filtering"""
    
    st.markdown("### 📋 Alumni Directory")
    
    # Get alumni data
    alumni_list = get_all_alumni()
    
    if not alumni_list:
        st.info("No alumni records found.")
        return
    
    # Filtering options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get unique batches
        batches = sorted(list(set([alumni.get('batch', 'Unknown') for alumni in alumni_list])))
        selected_batch = st.selectbox("Filter by Batch", ["All"] + [str(b) for b in batches])
    
    with col2:
        # Get unique branches
        branches = sorted(list(set([alumni.get('branch', 'Unknown') for alumni in alumni_list])))
        selected_branch = st.selectbox("Filter by Branch", ["All"] + branches)
    
    with col3:
        # Search by name or company
        search_term = st.text_input("Search by Name/Company", placeholder="Enter search term")
    
    # Filter alumni
    filtered_alumni = alumni_list
    
    if selected_batch != "All":
        filtered_alumni = [a for a in filtered_alumni if str(a.get('batch', '')) == selected_batch]
    
    if selected_branch != "All":
        filtered_alumni = [a for a in filtered_alumni if a.get('branch', '') == selected_branch]
    
    if search_term:
        search_term = search_term.lower()
        filtered_alumni = [a for a in filtered_alumni 
                          if search_term in a.get('name', '').lower() or 
                             search_term in a.get('company', '').lower()]
    
    st.markdown(f"**Showing {len(filtered_alumni)} alumni**")
    
    # Display alumni cards
    if filtered_alumni:
        for alumni in filtered_alumni:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                
                with col1:
                    st.markdown(f"**{alumni.get('name', 'N/A')}**")
                    st.caption(f"Batch: {alumni.get('batch', 'N/A')} | {alumni.get('branch', 'N/A')}")
                
                with col2:
                    st.markdown("**Current Company:**")
                    st.write(alumni.get('company', 'N/A'))
                
                with col3:
                    st.markdown("**Contact:**")
                    if alumni.get('email'):
                        st.write(f"📧 {alumni.get('email')}")
                    if alumni.get('phone'):
                        st.write(f"📱 {alumni.get('phone')}")
                
                with col4:
                    if alumni.get('linkedin'):
                        st.link_button("LinkedIn Profile", alumni.get('linkedin'))
                
                st.markdown("---")
    else:
        st.info("No alumni found matching the filters.")

def show_events():
    """Display upcoming events"""
    
    st.markdown("### 📅 Upcoming Events")
    
    events = get_all_events()
    
    if not events:
        st.info("No upcoming events scheduled.")
        return
    
    for event in events:
        with st.container():
            st.markdown(f"**{event.get('name', 'Untitled Event')}**")
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"📅 **Date:** {event.get('date', 'TBD')}")
            
            with col2:
                if event.get('description'):
                    st.markdown(f"**Description:** {event.get('description')}")
            
            st.markdown("---")

def show_profile():
    """Display student profile"""
    
    st.markdown("### 👤 My Profile")
    
    user_data = st.session_state.user_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Personal Information")
        st.write(f"**Name:** {user_data.get('name', 'N/A')}")
        st.write(f"**Email:** {user_data.get('email', 'N/A')}")
        st.write(f"**Phone:** {user_data.get('phone', 'N/A')}")
        st.write(f"**Batch:** {user_data.get('batch', 'N/A')}")
        st.write(f"**Branch:** {user_data.get('branch', 'N/A')}")
    
    with col2:
        st.markdown("#### Professional Information")
        st.write(f"**Current Company:** {user_data.get('current_company', 'N/A')}")
        st.write(f"**Designation:** {user_data.get('designation', 'N/A')}")
        st.write(f"**Working Status:** {user_data.get('working_status', 'N/A')}")
        st.write(f"**Location:** {user_data.get('location', 'N/A')}")
        if user_data.get('linkedin'):
            st.link_button("LinkedIn Profile", user_data.get('linkedin'))
