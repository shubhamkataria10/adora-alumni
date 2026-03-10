import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.database import (get_all_alumni, add_alumni, update_alumni, delete_alumni,
                           get_all_events, add_event)
from utils.auth import logout

def show_admin_dashboard():
    """Display admin dashboard"""
    
    if not st.session_state.admin_authenticated:
        st.session_state.page = 'landing'
        st.rerun()
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("👨‍💼 Admin Dashboard")
    with col2:
        if st.button("Logout", type="secondary"):
            logout()
    
    st.markdown("---")
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["👥 Manage Alumni", "📅 Manage Events", "📊 Statistics"])
    
    with tab1:
        manage_alumni()
    
    with tab2:
        manage_events()
    
    with tab3:
        show_statistics()

def manage_alumni():
    """Alumni management interface"""
    
    st.markdown("### 👥 Alumni Management")
    
    # Sub-tabs for alumni management
    subtab1, subtab2, subtab3 = st.tabs(["Add Alumni", "View/Edit Alumni", "Bulk Operations"])
    
    with subtab1:
        add_alumni_form()
    
    with subtab2:
        view_edit_alumni()
    
    with subtab3:
        bulk_operations()

def add_alumni_form():
    """Form to add new alumni"""
    
    st.markdown("#### Add New Alumni")
    
    with st.form("add_alumni_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter full name")
            email = st.text_input("Email Address", placeholder="Enter email")
            phone = st.text_input("Phone Number", placeholder="Enter phone number")
            batch = st.number_input("Batch Year *", min_value=1950, max_value=2030, value=2020)
        
        with col2:
            branch = st.selectbox("Branch *", 
                                ["Computer Science", "Electronics", "Mechanical", "Civil", 
                                 "Electrical", "Chemical", "Information Technology", "Other"])
            company = st.text_input("Current Company", placeholder="Enter current company")
            designation = st.text_input("Designation", placeholder="Enter designation")
            linkedin = st.text_input("LinkedIn Profile", placeholder="LinkedIn URL")
        
        location = st.text_input("Current Location", placeholder="Enter location")
        
        submitted = st.form_submit_button("Add Alumni", type="primary")
        
        if submitted:
            if not all([name, batch, branch]):
                st.error("Please fill in all required fields marked with *")
            else:
                alumni_data = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'batch': batch,
                    'branch': branch,
                    'company': company,
                    'designation': designation,
                    'linkedin': linkedin,
                    'location': location
                }
                
                if add_alumni(alumni_data):
                    st.success("Alumni added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add alumni. Please try again.")

def view_edit_alumni():
    """View and edit existing alumni"""
    
    st.markdown("#### View/Edit Alumni")
    
    alumni_list = get_all_alumni()
    
    if not alumni_list:
        st.info("No alumni records found.")
        return
    
    # Search and filter
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("Search Alumni", placeholder="Search by name...")
    with col2:
        batch_filter = st.selectbox("Filter by Batch", 
                                   ["All"] + sorted(list(set([str(a.get('batch', '')) for a in alumni_list]))))
    
    # Filter alumni
    filtered_alumni = alumni_list
    if search_term:
        search_term = search_term.lower()
        filtered_alumni = [a for a in filtered_alumni if search_term in a.get('name', '').lower()]
    
    if batch_filter != "All":
        filtered_alumni = [a for a in filtered_alumni if str(a.get('batch', '')) == batch_filter]
    
    st.markdown(f"**Found {len(filtered_alumni)} alumni**")
    
    # Display alumni in expandable sections
    for alumni in filtered_alumni:
        with st.expander(f"{alumni.get('name', 'Unknown')} - {alumni.get('batch', 'N/A')} - {alumni.get('branch', 'N/A')}"):
            
            # Edit form
            with st.form(f"edit_alumni_{alumni.get('id')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Name", value=alumni.get('name', ''))
                    email = st.text_input("Email", value=alumni.get('email', ''))
                    phone = st.text_input("Phone", value=alumni.get('phone', ''))
                    batch = st.number_input("Batch", value=int(alumni.get('batch', 2020)))
                
                with col2:
                    branch = st.selectbox("Branch", 
                                        ["Computer Science", "Electronics", "Mechanical", "Civil", 
                                         "Electrical", "Chemical", "Information Technology", "Other"],
                                        index=0 if alumni.get('branch') not in ["Computer Science", "Electronics", "Mechanical", "Civil", "Electrical", "Chemical", "Information Technology", "Other"] 
                                        else ["Computer Science", "Electronics", "Mechanical", "Civil", "Electrical", "Chemical", "Information Technology", "Other"].index(alumni.get('branch', 'Computer Science')))
                    company = st.text_input("Company", value=alumni.get('company', ''))
                    designation = st.text_input("Designation", value=alumni.get('designation', ''))
                    linkedin = st.text_input("LinkedIn", value=alumni.get('linkedin', ''))
                
                location = st.text_input("Location", value=alumni.get('location', ''))
                
                col_update, col_delete = st.columns(2)
                
                with col_update:
                    update_submitted = st.form_submit_button("Update", type="primary")
                
                with col_delete:
                    delete_submitted = st.form_submit_button("Delete", type="secondary")
                
                if update_submitted:
                    updated_data = {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'batch': batch,
                        'branch': branch,
                        'company': company,
                        'designation': designation,
                        'linkedin': linkedin,
                        'location': location
                    }
                    
                    if update_alumni(alumni.get('id'), updated_data):
                        st.success("Alumni updated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update alumni.")
                
                if delete_submitted:
                    if delete_alumni(alumni.get('id')):
                        st.success("Alumni deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete alumni.")

def bulk_operations():
    """Bulk operations for alumni data"""
    
    st.markdown("#### Bulk Operations")
    
    alumni_list = get_all_alumni()
    
    if alumni_list:
        # Export functionality
        df = pd.DataFrame(alumni_list)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📥 Export Alumni Data (CSV)",
            data=csv,
            file_name=f"alumni_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    st.markdown("---")
    
    # Import functionality
    st.markdown("**Import Alumni Data:**")
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Preview of uploaded data:")
            st.dataframe(df.head())
            
            if st.button("Import Data"):
                success_count = 0
                for _, row in df.iterrows():
                    alumni_data = row.to_dict()
                    if add_alumni(alumni_data):
                        success_count += 1
                
                st.success(f"Successfully imported {success_count} alumni records!")
                st.rerun()
        
        except Exception as e:
            st.error(f"Error reading file: {e}")

def manage_events():
    """Event management interface"""
    
    st.markdown("### 📅 Event Management")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Add New Event")
        
        with st.form("add_event_form"):
            event_name = st.text_input("Event Name *", placeholder="Enter event name")
            event_date = st.date_input("Event Date *", value=date.today())
            event_description = st.text_area("Description", placeholder="Enter event description")
            
            submitted = st.form_submit_button("Add Event", type="primary")
            
            if submitted:
                if not event_name:
                    st.error("Please enter event name")
                else:
                    event_data = {
                        'name': event_name,
                        'date': event_date.strftime('%Y-%m-%d'),
                        'description': event_description
                    }
                    
                    if add_event(event_data):
                        st.success("Event added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add event.")
    
    with col2:
        st.markdown("#### Existing Events")
        
        events = get_all_events()
        
        if not events:
            st.info("No events scheduled.")
        else:
            for event in events:
                with st.container():
                    st.markdown(f"**{event.get('name', 'Untitled')}**")
                    st.write(f"📅 Date: {event.get('date', 'TBD')}")
                    if event.get('description'):
                        st.write(f"Description: {event.get('description')}")
                    st.markdown("---")

def show_statistics():
    """Display platform statistics"""
    
    st.markdown("### 📊 Platform Statistics")
    
    alumni_list = get_all_alumni()
    events = get_all_events()
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Alumni", len(alumni_list))
    
    with col2:
        st.metric("Total Events", len(events))
    
    with col3:
        if alumni_list:
            companies = [a.get('company', '') for a in alumni_list if a.get('company')]
            unique_companies = len(set(companies))
            st.metric("Companies", unique_companies)
        else:
            st.metric("Companies", 0)
    
    with col4:
        if alumni_list:
            branches = [a.get('branch', '') for a in alumni_list if a.get('branch')]
            unique_branches = len(set(branches))
            st.metric("Branches", unique_branches)
        else:
            st.metric("Branches", 0)
    
    if alumni_list:
        st.markdown("---")
        
        # Alumni by batch
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Alumni by Batch")
            batch_data = {}
            for alumni in alumni_list:
                batch = str(alumni.get('batch', 'Unknown'))
                batch_data[batch] = batch_data.get(batch, 0) + 1
            
            if batch_data:
                df_batch = pd.DataFrame(list(batch_data.items()), columns=['Batch', 'Count'])
                st.bar_chart(df_batch.set_index('Batch')['Count'])
        
        with col2:
            st.markdown("#### Alumni by Branch")
            branch_data = {}
            for alumni in alumni_list:
                branch = alumni.get('branch', 'Unknown')
                branch_data[branch] = branch_data.get(branch, 0) + 1
            
            if branch_data:
                df_branch = pd.DataFrame(list(branch_data.items()), columns=['Branch', 'Count'])
                st.bar_chart(df_branch.set_index('Branch')['Count'])
