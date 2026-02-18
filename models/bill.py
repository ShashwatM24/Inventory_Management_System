"""
Bill model for invoice generation and management
"""
from datetime import datetime
from bson import ObjectId
from config.database import get_database
import random


class Bill:
    """Bill model for invoice management"""
    
    @staticmethod
    def generate_bill_number():
        """Generate unique bill number"""
        timestamp = datetime.now().strftime("%Y%m%d")
        random_part = random.randint(1000, 9999)
        return f"INV-{timestamp}-{random_part}"
    
    @staticmethod
    def create_bill(customer_name, customer_contact, items, tax_rate=0.18, discount=0, created_by=None):
        """
        Create a new bill
        
        Args:
            customer_name: Customer name
            customer_contact: Customer contact number
            items: List of items [{product_id, name, quantity, price, total}]
            tax_rate: Tax rate (default 18% GST)
            discount: Discount amount
            created_by: User ID who created the bill
        
        Returns:
            Bill ID if successful, None otherwise
        """
        db = get_database()
        
        # Generate unique bill number
        bill_number = Bill.generate_bill_number()
        while db.bills.find_one({"bill_number": bill_number}):
            bill_number = Bill.generate_bill_number()
        
        # Calculate totals
        subtotal = sum(item['total'] for item in items)
        tax = subtotal * tax_rate
        total = subtotal + tax - discount
        
        bill_doc = {
            "bill_number": bill_number,
            "customer_name": customer_name,
            "customer_contact": customer_contact,
            "items": items,
            "subtotal": round(subtotal, 2),
            "tax_rate": tax_rate,
            "tax": round(tax, 2),
            "discount": round(discount, 2),
            "total": round(total, 2),
            "created_at": datetime.now(),
            "created_by": ObjectId(created_by) if created_by else None
        }
        
        result = db.bills.insert_one(bill_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all_bills(limit=100):
        """Get all bills"""
        db = get_database()
        return list(db.bills.find().sort("created_at", -1).limit(limit))
    
    @staticmethod
    def get_bill_by_id(bill_id):
        """Get bill by ID"""
        db = get_database()
        return db.bills.find_one({"_id": ObjectId(bill_id)})
    
    @staticmethod
    def get_bill_by_number(bill_number):
        """Get bill by bill number"""
        db = get_database()
        return db.bills.find_one({"bill_number": bill_number})
    
    @staticmethod
    def search_bills(search_term):
        """Search bills by customer name or bill number"""
        db = get_database()
        return list(db.bills.find({
            "$or": [
                {"customer_name": {"$regex": search_term, "$options": "i"}},
                {"bill_number": {"$regex": search_term, "$options": "i"}},
                {"customer_contact": {"$regex": search_term, "$options": "i"}}
            ]
        }).sort("created_at", -1))
    
    @staticmethod
    def get_bills_by_date_range(start_date, end_date):
        """Get bills within date range"""
        db = get_database()
        return list(db.bills.find({
            "created_at": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).sort("created_at", -1))
    
    @staticmethod
    def delete_bill(bill_id):
        """Delete bill"""
        db = get_database()
        return db.bills.delete_one({"_id": ObjectId(bill_id)})
    
    @staticmethod
    def get_total_sales(start_date=None, end_date=None):
        """Calculate total sales"""
        db = get_database()
        
        query = {}
        if start_date and end_date:
            query["created_at"] = {"$gte": start_date, "$lte": end_date}
        
        pipeline = [
            {"$match": query},
            {"$group": {"_id": None, "total_sales": {"$sum": "$total"}}}
        ]
        
        result = list(db.bills.aggregate(pipeline))
        return result[0]['total_sales'] if result else 0
