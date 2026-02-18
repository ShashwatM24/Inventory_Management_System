"""
Supplier model for supplier management
"""
from datetime import datetime
from bson import ObjectId
from config.database import get_database


class Supplier:
    """Supplier model"""
    
    @staticmethod
    def create_supplier(name, contact_person, email, phone, address, notes=""):
        """
        Create a new supplier
        
        Args:
            name: Supplier company name
            contact_person: Contact person name
            email: Email address
            phone: Phone number
            address: Physical address
            notes: Optional notes
        
        Returns:
            Supplier ID if successful, None otherwise
        """
        db = get_database()
        
        supplier_doc = {
            "name": name,
            "contact_person": contact_person,
            "email": email,
            "phone": phone,
            "address": address,
            "notes": notes,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        result = db.suppliers.insert_one(supplier_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all_suppliers():
        """Get all suppliers"""
        db = get_database()
        return list(db.suppliers.find())
    
    @staticmethod
    def get_supplier_by_id(supplier_id):
        """Get supplier by ID"""
        db = get_database()
        return db.suppliers.find_one({"_id": ObjectId(supplier_id)})
    
    @staticmethod
    def update_supplier(supplier_id, updates):
        """Update supplier information"""
        db = get_database()
        updates['updated_at'] = datetime.now()
        return db.suppliers.update_one(
            {"_id": ObjectId(supplier_id)},
            {"$set": updates}
        )
    
    @staticmethod
    def delete_supplier(supplier_id):
        """Delete supplier"""
        db = get_database()
        return db.suppliers.delete_one({"_id": ObjectId(supplier_id)})
    
    @staticmethod
    def search_suppliers(search_term):
        """Search suppliers by name, contact person, or email"""
        db = get_database()
        return list(db.suppliers.find({
            "$or": [
                {"name": {"$regex": search_term, "$options": "i"}},
                {"contact_person": {"$regex": search_term, "$options": "i"}},
                {"email": {"$regex": search_term, "$options": "i"}}
            ]
        }))
