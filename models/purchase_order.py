
"""
Purchase Order model for managing procurement
"""
from datetime import datetime
from bson import ObjectId
from config.database import get_database

class PurchaseOrder:
    """Purchase Order model"""
    
    @staticmethod
    def create_po(po_number, supplier_id, supplier_name, order_date, expected_delivery, 
                  items, status="Draft", notes="", shipping_address="", created_by=None):
        """
        Create a new purchase order
        """
        db = get_database()
        
        # Calculate totals
        total_amount = sum(item['total'] for item in items)
        
        po_doc = {
            "po_number": po_number,
            "supplier_id": ObjectId(supplier_id) if supplier_id else None,
            "supplier_name": supplier_name,
            "order_date": datetime.combine(order_date, datetime.min.time()),
            "expected_delivery": datetime.combine(expected_delivery, datetime.min.time()) if expected_delivery else None,
            "items": items,
            "total_amount": float(total_amount),
            "status": status,
            "notes": notes,
            "shipping_address": shipping_address,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "created_by": ObjectId(created_by) if created_by else None
        }
        
        result = db.purchase_orders.insert_one(po_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all_pos(limit=100):
        """Get all purchase orders"""
        db = get_database()
        return list(db.purchase_orders.find().sort("created_at", -1).limit(limit))
    
    @staticmethod
    def get_po_by_id(po_id):
        """Get PO by ID"""
        db = get_database()
        return db.purchase_orders.find_one({"_id": ObjectId(po_id)})
    
    @staticmethod
    def update_status(po_id, status):
        """Update PO status"""
        db = get_database()
        db.purchase_orders.update_one(
            {"_id": ObjectId(po_id)},
            {
                "$set": {
                    "status": status,
                    "updated_at": datetime.now()
                }
            }
        )
