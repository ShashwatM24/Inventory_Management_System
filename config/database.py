"""
Database configuration and connection management
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "inventory_management")

# Global database connection
_client = None
_db = None


def get_database():
    """
    Get MongoDB database instance with connection pooling
    Returns the database object
    """
    global _client, _db
    
    if _db is None:
        try:
            _client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            # Test connection
            _client.admin.command('ping')
            _db = _client[DATABASE_NAME]
            print(f"✅ Connected to MongoDB: {DATABASE_NAME}")
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    return _db


def init_db():
    """
    Initialize database with indexes for optimized queries
    """
    db = get_database()
    
    # Create indexes for better performance
    try:
        # Users collection
        db.users.create_index("username", unique=True)
        db.users.create_index("email", unique=True)
        
        # Products collection
        db.products.create_index("sku", unique=True)
        db.products.create_index("name")
        db.products.create_index("category")
        db.products.create_index("quantity")
        
        # Bills collection
        db.bills.create_index("bill_number", unique=True)
        db.bills.create_index("created_at")
        
        # Suppliers collection
        db.suppliers.create_index("name")
        
        print("✅ Database indexes created successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not create indexes: {e}")


def close_connection():
    """
    Close MongoDB connection
    """
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        print("✅ MongoDB connection closed")


# Collection names
COLLECTIONS = {
    'users': 'users',
    'products': 'products',
    'categories': 'categories',
    'bills': 'bills',
    'suppliers': 'suppliers',
    'packages': 'packages',
    'transfers': 'transfers',
    'stock_movements': 'stock_movements'
}
