"""
Database cleanup utility to fix user schema issues
"""
from config.database import get_database


def cleanup_invalid_users():
    """
    Remove users with invalid schema (missing required fields)
    """
    db = get_database()
    
    required_fields = ['username', 'email', 'password_hash', 'role']
    
    # Find all users
    all_users = list(db.users.find({}))
    
    invalid_count = 0
    for user in all_users:
        missing_fields = [field for field in required_fields if field not in user]
        
        if missing_fields:
            print(f"⚠️ Found invalid user: {user.get('_id')} - Missing: {missing_fields}")
            # Delete invalid user
            db.users.delete_one({"_id": user['_id']})
            invalid_count += 1
            print(f"✅ Deleted invalid user: {user.get('_id')}")
    
    if invalid_count == 0:
        print("✅ No invalid users found")
    else:
        print(f"✅ Cleaned up {invalid_count} invalid user(s)")
    
    return invalid_count


def list_all_users():
    """
    List all users in the database with their fields
    """
    db = get_database()
    
    users = list(db.users.find({}, {"password_hash": 0}))
    
    if not users:
        print("No users found in database")
        return
    
    print(f"\n📋 Total users: {len(users)}")
    for user in users:
        print(f"\nUser ID: {user.get('_id')}")
        print(f"  Username: {user.get('username', 'MISSING')}")
        print(f"  Email: {user.get('email', 'MISSING')}")
        print(f"  Role: {user.get('role', 'MISSING')}")
        print(f"  Created: {user.get('created_at', 'MISSING')}")


if __name__ == "__main__":
    print("=== Database Cleanup Utility ===\n")
    
    print("1. Listing all users...")
    list_all_users()
    
    print("\n2. Cleaning up invalid users...")
    cleanup_invalid_users()
    
    print("\n3. Final user list...")
    list_all_users()
