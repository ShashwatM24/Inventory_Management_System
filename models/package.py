
"""
Package model for shipment tracking
"""
from datetime import datetime
from bson import ObjectId
from config.database import get_database

class Package:
    """Package model"""
    
    @staticmethod
    def create_package(tracking_number, carrier, status="Pending", destination="", notes="", created_by=None):
        """
        Create a new package
        """
        db = get_database()
        
        package_doc = {
            "tracking_number": tracking_number,
            "carrier": carrier,
            "status": status,
            "destination": destination,
            "notes": notes,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "created_by": ObjectId(created_by) if created_by else None,
            "tracking_history": []
        }
        
        result = db.packages.insert_one(package_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all_packages(limit=100):
        """Get all packages"""
        db = get_database()
        return list(db.packages.find().sort("created_at", -1).limit(limit))
    
    @staticmethod
    def update_status(package_id, status, location=None, details=None):
        """Update package status"""
        db = get_database()
        
        update_doc = {
            "status": status,
            "updated_at": datetime.now()
        }
        
        # Add to history
        history_entry = {
            "status": status,
            "location": location,
            "details": details,
            "timestamp": datetime.now()
        }
        
        db.packages.update_one(
            {"_id": ObjectId(package_id)},
            {
                "$set": update_doc,
                "$push": {"tracking_history": history_entry}
            }
        )
