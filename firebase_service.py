import pyrebase
import streamlit as st
from config import FIREBASE_CONFIG, COLLECTIONS
import json

class FirebaseService:
    def __init__(self):
        self.firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
    
    def authenticate_admin(self, username, password):
        """Authenticate admin user"""
        try:
            # In a real app, you'd store admin credentials in Firebase
            # For demo purposes, using hardcoded credentials
            if username == "admin" and password == "admin123":
                return True
            return False
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return False
    
    def add_student(self, student_data):
        """Add a new student to the database"""
        try:
            self.db.child(COLLECTIONS["students"]).push(student_data)
            return True
        except Exception as e:
            st.error(f"Error adding student: {str(e)}")
            return False
    
    def get_all_students(self):
        """Get all students from the database"""
        try:
            students = self.db.child(COLLECTIONS["students"]).get()
            if students.val():
                return students.val()
            return {}
        except Exception as e:
            st.error(f"Error fetching students: {str(e)}")
            return {}
    
    def update_student(self, student_id, student_data):
        """Update student information"""
        try:
            self.db.child(COLLECTIONS["students"]).child(student_id).update(student_data)
            return True
        except Exception as e:
            st.error(f"Error updating student: {str(e)}")
            return False
    
    def delete_student(self, student_id):
        """Delete a student"""
        try:
            self.db.child(COLLECTIONS["students"]).child(student_id).remove()
            return True
        except Exception as e:
            st.error(f"Error deleting student: {str(e)}")
            return False
    
    def add_event(self, event_data):
        """Add a new event"""
        try:
            self.db.child(COLLECTIONS["events"]).push(event_data)
            return True
        except Exception as e:
            st.error(f"Error adding event: {str(e)}")
            return False
    
    def get_all_events(self):
        """Get all events from the database"""
        try:
            events = self.db.child(COLLECTIONS["events"]).get()
            if events.val():
                return events.val()
            return {}
        except Exception as e:
            st.error(f"Error fetching events: {str(e)}")
            return {}
    
    def update_event(self, event_id, event_data):
        """Update event information"""
        try:
            self.db.child(COLLECTIONS["events"]).child(event_id).update(event_data)
            return True
        except Exception as e:
            st.error(f"Error updating event: {str(e)}")
            return False
    
    def delete_event(self, event_id):
        """Delete an event"""
        try:
            self.db.child(COLLECTIONS["events"]).child(event_id).remove()
            return True
        except Exception as e:
            st.error(f"Error deleting event: {str(e)}")
            return False
