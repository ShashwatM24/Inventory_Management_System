
import sys
import os
sys.path.append(os.getcwd())

from config.database import get_database
import pymongo

def fix_package_indexes():
    print("🔌 Connecting to database...")
    db = get_database()
    
    # Fix Packages Collection Indexes
    print("🛠️ Fixing 'packages' collection indexes...")
    try:
        # List existing indexes
        indexes = list(db.packages.list_indexes())
        print(f"   Current indexes: {[i['name'] for i in indexes]}")
        
        # Drop the incorrect index if it exists
        if any(i['name'] == 'trackingNumber_1' for i in indexes):
            print("   🗑️ Dropping incorrect index 'trackingNumber_1'...")
            db.packages.drop_index('trackingNumber_1')
            print("   ✅ Dropped 'trackingNumber_1'")
        
        # Create the correct index
        print("   ➕ Creating correct index 'tracking_number_1'...")
        db.packages.create_index("tracking_number", unique=True)
        print("   ✅ Created unique index on 'tracking_number'")
        
    except Exception as e:
        print(f"   ❌ Error fixing packages indexes: {e}")

    print("\n✨ Database index fix completed!")

if __name__ == "__main__":
    fix_package_indexes()
