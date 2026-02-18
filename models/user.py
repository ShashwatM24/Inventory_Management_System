"""
User model for authentication and user management
"""
import bcrypt
from datetime import datetime
from bson import ObjectId
from config.database import get_database


class User:
    """User model for authentication"""
    
    @staticmethod
    def create_user(username, email, password, role="staff"):
        """
        Create a new user with hashed password
        
        Args:
            username: User's username
            email: User's email
            password: Plain text password
            role: User role (admin, manager, staff)
        
        Returns:
            User ID if successful, None otherwise
        """
        db = get_database()
        
        # Check if user already exists
        if db.users.find_one({"$or": [{"username": username}, {"email": email}]}):
            return None
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user document
        user_doc = {
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "role": role,
            "created_at": datetime.now(),
            "last_login": None
        }
        
        result = db.users.insert_one(user_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def authenticate(username, password):
        """
        Authenticate user with username and password
        
        Args:
            username: Username or email
            password: Plain text password
        
        Returns:
            User document if authenticated, None otherwise
        """
        db = get_database()
        
        # Find user by username or email
        user = db.users.find_one({
            "$or": [{"username": username}, {"email": username}]
        })
        
        if not user:
            return None
        
        # Validate user document has required fields
        required_fields = ['username', 'email', 'password_hash', 'role']
        missing_fields = [field for field in required_fields if field not in user]
        
        if missing_fields:
            print(f"⚠️ Warning: User document missing fields: {missing_fields}")
            return None
        
        # Verify password
        try:
            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
                # Update last login
                db.users.update_one(
                    {"_id": user['_id']},
                    {"$set": {"last_login": datetime.now()}}
                )
                return user
        except (ValueError, TypeError) as e:
            print(f"⚠️ Password verification error: {e}")
            return None
        
        return None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        db = get_database()
        return db.users.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        db = get_database()
        return db.users.find_one({"username": username})
    
    @staticmethod
    def update_user(user_id, updates):
        """Update user information"""
        db = get_database()
        return db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updates}
        )
    
    @staticmethod
    def delete_user(user_id):
        """Delete user"""
        db = get_database()
        return db.users.delete_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        db = get_database()
        return list(db.users.find({}, {"password_hash": 0}))  # Exclude password hash
