
"""
Sales Order model for managing customer orders
"""
from datetime import datetime
from bson import ObjectId
from config.database import get_database

class SalesOrder:
    """Sales Order model"""
    
    @staticmethod
    def create_order(order_number, customer_name, order_date, delivery_date, items, notes="", created_by=None):
        """
        Create a new sales order
        """
        db = get_database()
        
        # Calculate totals
        total_amount = sum(item['total'] for item in items)
        
        order_doc = {
            "order_number": order_number,
            "customer_name": customer_name,
            "order_date": datetime.combine(order_date, datetime.min.time()),
            "delivery_date": datetime.combine(delivery_date, datetime.min.time()) if delivery_date else None,
            "items": items,
            "total_amount": float(total_amount),
            "notes": notes,
            "status": "Pending",
            "created_at": datetime.now(),
            "created_by": ObjectId(created_by) if created_by else None
        }
        
        result = db.sales_orders.insert_one(order_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all_orders(limit=100):
        """Get all sales orders"""
        db = get_database()
        return list(db.sales_orders.find().sort("created_at", -1).limit(limit))
    
    @staticmethod
    def get_order_by_id(order_id):
        """Get order by ID"""
        db = get_database()
        return db.sales_orders.find_one({"_id": ObjectId(order_id)})
