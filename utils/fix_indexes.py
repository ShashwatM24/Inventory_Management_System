
import sys
import os
sys.path.append(os.getcwd())

from config.database import get_database
import pymongo

def fix_indexes():
    print("🔌 Connecting to database...")
    db = get_database()
    
    # Fix Bills Collection Indexes
    print("🛠️ Fixing 'bills' collection indexes...")
    try:
        # List existing indexes
        indexes = list(db.bills.list_indexes())
        print(f"   Current indexes: {[i['name'] for i in indexes]}")
        
        # Drop the incorrect index if it exists
        if any(i['name'] == 'billNumber_1' for i in indexes):
            print("   🗑️ Dropping incorrect index 'billNumber_1'...")
            db.bills.drop_index('billNumber_1')
            print("   ✅ Dropped 'billNumber_1'")
        
        # Create the correct index
        print("   ➕ Creating correct index 'bill_number_1'...")
        db.bills.create_index("bill_number", unique=True)
        print("   ✅ Created unique index on 'bill_number'")
        
    except Exception as e:
        print(f"   ❌ Error fixing bills indexes: {e}")

    print("\n✨ Database index fix completed!")

if __name__ == "__main__":
    fix_indexes()
