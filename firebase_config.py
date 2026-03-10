import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    if not firebase_admin._apps:
        try:
            # Try to get Firebase credentials from environment variable
            firebase_creds = os.getenv('FIREBASE_CREDENTIALS')
            if firebase_creds:
                # Parse JSON credentials from environment variable
                cred_dict = json.loads(firebase_creds)
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                print("Firebase initialized with provided credentials")
            else:
                # Skip Firebase initialization for development
                print("No Firebase credentials found. Using in-memory storage for development.")
                return
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            print("Running in development mode without Firebase backend.")

def get_firestore_client():
    """Get Firestore database client"""
    try:
        # Check if Firebase is initialized
        if not firebase_admin._apps:
            print("Firebase not initialized - using in-memory storage for development")
            return None
        return firestore.client()
    except Exception as e:
        print(f"Error getting Firestore client: {e}")
        print("Firebase unavailable - using in-memory storage for development")
        return None
