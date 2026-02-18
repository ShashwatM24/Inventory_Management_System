
"""
Invoice model for managing customer invoices
"""
from datetime import datetime
from bson import ObjectId
from config.database import get_database

class Invoice:
    """Invoice model"""
    
    @staticmethod
    def create_invoice(invoice_number, customer_name, invoice_date, due_date, items, 
                       tax_rate=0.0, status="Draft", notes="", sales_order_id=None, created_by=None):
        """
        Create a new invoice
        """
        db = get_database()
        
        # Calculate totals
        subtotal = sum(item['total'] for item in items)
        tax_amount = subtotal * (tax_rate / 100)
        total_amount = subtotal + tax_amount
        
        invoice_doc = {
            "invoice_number": invoice_number,
            "customer_name": customer_name,
            "sales_order_id": ObjectId(sales_order_id) if sales_order_id else None,
            "invoice_date": datetime.combine(invoice_date, datetime.min.time()),
            "due_date": datetime.combine(due_date, datetime.min.time()) if due_date else None,
            "items": items,
            "subtotal": float(subtotal),
            "tax_rate": float(tax_rate),
            "tax_amount": float(tax_amount),
            "total_amount": float(total_amount),
            "status": status,
            "notes": notes,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "created_by": ObjectId(created_by) if created_by else None
        }
        
        result = db.invoices.insert_one(invoice_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all_invoices(limit=100):
        """Get all invoices"""
        db = get_database()
        return list(db.invoices.find().sort("created_at", -1).limit(limit))
    
    @staticmethod
    def get_invoice_by_id(invoice_id):
        """Get invoice by ID"""
        db = get_database()
        return db.invoices.find_one({"_id": ObjectId(invoice_id)})
    
    @staticmethod
    def update_status(invoice_id, status):
        """Update invoice status"""
        db = get_database()
        db.invoices.update_one(
            {"_id": ObjectId(invoice_id)},
            {
                "$set": {
                    "status": status,
                    "updated_at": datetime.now()
                }
            }
        )
