import streamlit as st
from firebase_config import get_firestore_client
from datetime import datetime
import uuid
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# In-memory storage for development when Firebase is not available
_memory_storage = {
    'students': {},
    'parents': {},
    'children': {},
    'alumni': {},
    'events': {},
    'admin': {
        'credentials': {
            'username': 'admin',
            'password': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'  # admin
        }
    }
}

def get_db_connection():
    """Get PostgreSQL database connection"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
            return conn
        else:
            print("No DATABASE_URL found, using in-memory storage")
            return None
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def init_database():
    """Initialize database tables"""
    try:
        conn = get_db_connection()
        if not conn:
            print("Database not available, using in-memory storage")
            return False
        
        with conn.cursor() as cur:
            # Create students table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    email VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    phone VARCHAR(50),
                    batch INTEGER NOT NULL,
                    branch VARCHAR(100) NOT NULL,
                    linkedin VARCHAR(500),
                    current_company VARCHAR(255),
                    designation VARCHAR(255),
                    working_status VARCHAR(100),
                    location VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create alumni table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS alumni (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255),
                    phone VARCHAR(50),
                    batch INTEGER NOT NULL,
                    branch VARCHAR(100) NOT NULL,
                    company VARCHAR(255),
                    designation VARCHAR(255),
                    linkedin VARCHAR(500),
                    location VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create events table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(255) NOT NULL,
                    date DATE NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create admin table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS admin_credentials (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert default admin credentials if not exists
            cur.execute("""
                INSERT INTO admin_credentials (username, password) 
                VALUES ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918')
                ON CONFLICT (username) DO NOTHING
            """)
            
            conn.commit()
            print("Database initialized successfully")
            return True
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_firestore_db():
    """Get Firestore database instance"""
    return get_firestore_client()

def _use_database():
    """Check if we should use PostgreSQL database"""
    return get_db_connection() is not None

def create_student(student_data):
    """Create a new student record"""
    try:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO students (email, name, phone, batch, branch, linkedin, 
                                        current_company, designation, working_status, location)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    student_data['email'],
                    student_data['name'],
                    student_data.get('phone', ''),
                    student_data['batch'],
                    student_data['branch'],
                    student_data.get('linkedin', ''),
                    student_data.get('current_company', ''),
                    student_data.get('designation', ''),
                    student_data.get('working_status', ''),
                    student_data.get('location', '')
                ))
                conn.commit()
                print(f"Student created in database: {student_data['email']}")
                return True
        else:
            # Fallback to in-memory storage
            student_data['created_at'] = datetime.now().isoformat()
            _memory_storage['students'][student_data['email']] = student_data
            print(f"Student created in memory storage: {student_data['email']}")
            return True
    except Exception as e:
        print(f"Error creating student: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_student_by_email(email):
    """Get student by email"""
    try:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM students WHERE email = %s", (email,))
                result = cur.fetchone()
                return dict(result) if result else None
        else:
            # Fallback to in-memory storage
            return _memory_storage['students'].get(email)
    except Exception as e:
        print(f"Error getting student: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_all_alumni():
    """Get all alumni records"""
    try:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM alumni ORDER BY created_at DESC")
                results = cur.fetchall()
                return [dict(row) for row in results]
        else:
            # Fallback to in-memory storage
            alumni_list = []
            for alumni_id, alumni_data in _memory_storage['alumni'].items():
                alumni_data_copy = alumni_data.copy()
                alumni_data_copy['id'] = alumni_id
                alumni_list.append(alumni_data_copy)
            return alumni_list
    except Exception as e:
        print(f"Error getting alumni: {e}")
        return []
    finally:
        if conn:
            conn.close()

def add_alumni(alumni_data):
    """Add new alumni record"""
    try:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO alumni (name, email, phone, batch, branch, company, 
                                      designation, linkedin, location)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    alumni_data['name'],
                    alumni_data.get('email', ''),
                    alumni_data.get('phone', ''),
                    alumni_data['batch'],
                    alumni_data['branch'],
                    alumni_data.get('company', ''),
                    alumni_data.get('designation', ''),
                    alumni_data.get('linkedin', ''),
                    alumni_data.get('location', '')
                ))
                result = cur.fetchone()
                conn.commit()
                print(f"Alumni added to database: {result['id']}")
                return True
        else:
            # Fallback to in-memory storage
            alumni_id = str(uuid.uuid4())
            alumni_data['created_at'] = datetime.now().isoformat()
            _memory_storage['alumni'][alumni_id] = alumni_data
            print(f"Alumni added in memory storage: {alumni_id}")
            return True
    except Exception as e:
        print(f"Error adding alumni: {e}")
        return False
    finally:
        if conn:
            conn.close()

def update_alumni(alumni_id, alumni_data):
    """Update existing alumni record"""
    try:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE alumni SET name = %s, email = %s, phone = %s, batch = %s, 
                                    branch = %s, company = %s, designation = %s, 
                                    linkedin = %s, location = %s
                    WHERE id = %s
                """, (
                    alumni_data['name'],
                    alumni_data.get('email', ''),
                    alumni_data.get('phone', ''),
                    alumni_data['batch'],
                    alumni_data['branch'],
                    alumni_data.get('company', ''),
                    alumni_data.get('designation', ''),
                    alumni_data.get('linkedin', ''),
                    alumni_data.get('location', ''),
                    alumni_id
                ))
                conn.commit()
                return cur.rowcount > 0
        else:
            # Fallback to in-memory storage
            if alumni_id in _memory_storage['alumni']:
                _memory_storage['alumni'][alumni_id].update(alumni_data)
                return True
            return False
    except Exception as e:
        print(f"Error updating alumni: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_alumni(alumni_id):
    """Delete alumni record"""
    try:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM alumni WHERE id = %s", (alumni_id,))
                conn.commit()
                return cur.rowcount > 0
        else:
            # Fallback to in-memory storage
            if alumni_id in _memory_storage['alumni']:
                del _memory_storage['alumni'][alumni_id]
                return True
            return False
    except Exception as e:
        print(f"Error deleting alumni: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_all_events():
    """Get all events"""
    try:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM events ORDER BY date")
                results = cur.fetchall()
                return [dict(row) for row in results]
        else:
            # Fallback to in-memory storage
            events_list = []
            for event_id, event_data in _memory_storage['events'].items():
                event_data_copy = event_data.copy()
                event_data_copy['id'] = event_id
                events_list.append(event_data_copy)
            # Sort by date
            events_list.sort(key=lambda x: x.get('date', ''))
            return events_list
    except Exception as e:
        print(f"Error getting events: {e}")
        return []
    finally:
        if conn:
            conn.close()

def add_event(event_data):
    """Add new event"""
    try:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO events (name, date, description)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (
                    event_data['name'],
                    event_data['date'],
                    event_data.get('description', '')
                ))
                result = cur.fetchone()
                conn.commit()
                print(f"Event added to database: {result['id']}")
                return True
        else:
            # Fallback to in-memory storage
            event_id = str(uuid.uuid4())
            event_data['created_at'] = datetime.now().isoformat()
            _memory_storage['events'][event_id] = event_data
            print(f"Event added in memory storage: {event_id}")
            return True
    except Exception as e:
        print(f"Error adding event: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_admin_credentials():
    """Get admin credentials from database"""
    try:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username, password FROM admin_credentials LIMIT 1")
                result = cur.fetchone()
                if result:
                    return dict(result)
        
        # Fallback admin credentials
        return {
            'username': 'admin',
            'password': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'  # admin
        }
    except Exception as e:
        print(f"Error getting admin credentials: {e}")
        # Fallback admin credentials
        return {
            'username': 'admin',
            'password': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'  # admin
        }
    finally:
        if conn:
            conn.close()
