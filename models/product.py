"""
Product model for inventory management
Includes category management within the same model
"""
from datetime import datetime
from bson import ObjectId
from config.database import get_database
import random
import string


class Product:
    """Product model for inventory management"""
    
    @staticmethod
    def generate_sku(prefix="PRD"):
        """Generate unique SKU"""
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"{prefix}-{random_part}"
    
    @staticmethod
    def create_product(name, description, category, quantity, unit, price, cost, reorder_level, supplier_id=None):
        """
        Create a new product
        
        Args:
            name: Product name
            description: Product description
            category: Product category
            quantity: Initial stock quantity
            unit: Unit of measurement (pcs, kg, ltr, etc.)
            price: Selling price
            cost: Cost price
            reorder_level: Minimum stock level for alerts
            supplier_id: Optional supplier ID
        
        Returns:
            Product ID if successful, None otherwise
        """
        db = get_database()
        
        # Generate unique SKU
        sku = Product.generate_sku()
        while db.products.find_one({"sku": sku}):
            sku = Product.generate_sku()
        
        product_doc = {
            "sku": sku,
            "name": name,
            "description": description,
            "category": category,
            "quantity": quantity,
            "unit": unit,
            "price": float(price),
            "cost": float(cost),
            "reorder_level": reorder_level,
            "supplier_id": supplier_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        result = db.products.insert_one(product_doc)
        
        # Log stock movement
        Product.log_stock_movement(
            str(result.inserted_id),
            quantity,
            "initial_stock",
            "Initial stock added"
        )
        
        return str(result.inserted_id)
    
    @staticmethod
    def get_all_products(filters=None):
        """Get all products with optional filters"""
        db = get_database()
        query = filters if filters else {}
        return list(db.products.find(query))
    
    @staticmethod
    def get_product_by_id(product_id):
        """Get product by ID"""
        db = get_database()
        return db.products.find_one({"_id": ObjectId(product_id)})
    
    @staticmethod
    def get_product_by_sku(sku):
        """Get product by SKU"""
        db = get_database()
        return db.products.find_one({"sku": sku})
    
    @staticmethod
    def update_product(product_id, updates):
        """Update product information"""
        db = get_database()
        updates['updated_at'] = datetime.now()
        return db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": updates}
        )
    
    @staticmethod
    def update_stock(product_id, quantity_change, movement_type="adjustment", notes=""):
        """
        Update product stock quantity
        
        Args:
            product_id: Product ID
            quantity_change: Change in quantity (positive or negative)
            movement_type: Type of movement (sale, purchase, adjustment, etc.)
            notes: Optional notes
        
        Returns:
            True if successful, False otherwise
        """
        db = get_database()
        
        product = Product.get_product_by_id(product_id)
        if not product:
            return False
        
        # Handle both 'stock' and 'quantity' field names for compatibility
        current_stock = product.get('stock', product.get('quantity', 0))
        new_quantity = current_stock + quantity_change
        
        if new_quantity < 0:
            return False  # Cannot have negative stock
        
        # Update both fields to ensure consistency
        db.products.update_one(
            {"_id": ObjectId(product_id)},
            {
                "$set": {
                    "stock": new_quantity,
                    "quantity": new_quantity,
                    "updated_at": datetime.now()
                }
            }
        )
        
        # Log stock movement
        Product.log_stock_movement(product_id, quantity_change, movement_type, notes)
        
        return True
    
    @staticmethod
    def delete_product(product_id):
        """Delete product"""
        db = get_database()
        return db.products.delete_one({"_id": ObjectId(product_id)})
    
    @staticmethod
    def search_products(search_term):
        """Search products by name, SKU, category, or description with multi-term support"""
        db = get_database()
        
        terms = search_term.split()
        if not terms:
            return []
            
        # Create a list of regex conditions for each term
        # Each term must match at least one field (Name OR SKU OR Category OR Description)
        and_conditions = []
        for term in terms:
            term_regex = {"$regex": term, "$options": "i"}
            and_conditions.append({
                "$or": [
                    {"name": term_regex},
                    {"sku": term_regex},
                    {"category": term_regex},
                    {"description": term_regex}
                ]
            })
            
        return list(db.products.find({"$and": and_conditions}))
    
    @staticmethod
    def get_low_stock_items():
        """Get products with quantity below reorder level"""
        db = get_database()
        return list(db.products.find({
            "$expr": {"$lte": ["$quantity", "$reorder_level"]}
        }))
    
    @staticmethod
    def get_categories():
        """Get all unique categories"""
        db = get_database()
        return db.products.distinct("category")
    
    @staticmethod
    def get_products_by_category(category):
        """Get all products in a category"""
        db = get_database()
        return list(db.products.find({"category": category}))
    
    @staticmethod
    def log_stock_movement(product_id, quantity_change, movement_type, notes):
        """Log stock movement for tracking"""
        db = get_database()
        
        movement_doc = {
            "product_id": ObjectId(product_id),
            "quantity_change": quantity_change,
            "movement_type": movement_type,
            "notes": notes,
            "timestamp": datetime.now()
        }
        
        db.stock_movements.insert_one(movement_doc)
    
    @staticmethod
    def get_stock_movements(product_id=None, limit=50):
        """Get stock movement history"""
        db = get_database()
        query = {"product_id": ObjectId(product_id)} if product_id else {}
        return list(db.stock_movements.find(query).sort("timestamp", -1).limit(limit))
