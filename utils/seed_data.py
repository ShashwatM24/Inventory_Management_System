"""
Seed data generator for testing
"""
from models.user import User
from models.product import Product
from models.supplier import Supplier
from models.bill import Bill
import random


def create_demo_user():
    """Create demo admin user"""
    try:
        user_id = User.create_user(
            username="admin",
            email="admin@inventory.com",
            password="admin123",
            role="admin"
        )
        if user_id:
            print("✅ Demo user created: admin / admin123")
        else:
            print("ℹ️ Demo user already exists")
    except Exception as e:
        print(f"⚠️ Could not create demo user: {e}")


def create_demo_suppliers():
    """Create demo suppliers"""
    suppliers_data = [
        {
            "name": "Tech Solutions Pvt Ltd",
            "contact_person": "Rajesh Kumar",
            "email": "rajesh@techsolutions.com",
            "phone": "+91 9876543210",
            "address": "123 MG Road, Bangalore, Karnataka 560001",
            "notes": "Primary electronics supplier"
        },
        {
            "name": "Global Traders",
            "contact_person": "Priya Sharma",
            "email": "priya@globaltraders.com",
            "phone": "+91 9876543211",
            "address": "456 Park Street, Mumbai, Maharashtra 400001",
            "notes": "Wholesale supplier"
        },
        {
            "name": "Quality Goods Co.",
            "contact_person": "Amit Patel",
            "email": "amit@qualitygoods.com",
            "phone": "+91 9876543212",
            "address": "789 Ring Road, Delhi 110001",
            "notes": "Quality products at competitive prices"
        }
    ]
    
    supplier_ids = []
    for supplier_data in suppliers_data:
        supplier_id = Supplier.create_supplier(**supplier_data)
        if supplier_id:
            supplier_ids.append(supplier_id)
            print(f"✅ Created supplier: {supplier_data['name']}")
    
    return supplier_ids


def create_demo_products(supplier_ids):
    """Create demo products"""
    categories = ["Electronics", "Furniture", "Stationery", "Accessories", "Hardware"]
    
    products_data = [
        # Electronics
        {"name": "Laptop Dell XPS 15", "category": "Electronics", "quantity": 15, "unit": "pcs", "price": 85000, "cost": 75000, "reorder": 5},
        {"name": "Wireless Mouse Logitech", "category": "Electronics", "quantity": 50, "unit": "pcs", "price": 1200, "cost": 900, "reorder": 10},
        {"name": "USB-C Cable", "category": "Electronics", "quantity": 100, "unit": "pcs", "price": 300, "cost": 150, "reorder": 20},
        {"name": "Keyboard Mechanical", "category": "Electronics", "quantity": 30, "unit": "pcs", "price": 3500, "cost": 2800, "reorder": 10},
        {"name": "Monitor 24 inch", "category": "Electronics", "quantity": 8, "unit": "pcs", "price": 12000, "cost": 10000, "reorder": 5},
        
        # Furniture
        {"name": "Office Chair Ergonomic", "category": "Furniture", "quantity": 20, "unit": "pcs", "price": 8500, "cost": 6500, "reorder": 5},
        {"name": "Desk Wooden", "category": "Furniture", "quantity": 12, "unit": "pcs", "price": 15000, "cost": 12000, "reorder": 3},
        {"name": "Filing Cabinet", "category": "Furniture", "quantity": 8, "unit": "pcs", "price": 5500, "cost": 4500, "reorder": 3},
        
        # Stationery
        {"name": "A4 Paper Ream", "category": "Stationery", "quantity": 200, "unit": "pcs", "price": 250, "cost": 180, "reorder": 50},
        {"name": "Pen Blue", "category": "Stationery", "quantity": 500, "unit": "pcs", "price": 10, "cost": 5, "reorder": 100},
        {"name": "Notebook A5", "category": "Stationery", "quantity": 150, "unit": "pcs", "price": 50, "cost": 30, "reorder": 30},
        {"name": "Stapler Heavy Duty", "category": "Stationery", "quantity": 25, "unit": "pcs", "price": 350, "cost": 250, "reorder": 10},
        
        # Accessories
        {"name": "Laptop Bag", "category": "Accessories", "quantity": 40, "unit": "pcs", "price": 1500, "cost": 1000, "reorder": 10},
        {"name": "Phone Stand", "category": "Accessories", "quantity": 60, "unit": "pcs", "price": 450, "cost": 300, "reorder": 15},
        {"name": "Cable Organizer", "category": "Accessories", "quantity": 80, "unit": "pcs", "price": 200, "cost": 120, "reorder": 20},
        
        # Hardware
        {"name": "Screwdriver Set", "category": "Hardware", "quantity": 35, "unit": "pcs", "price": 800, "cost": 600, "reorder": 10},
        {"name": "Drill Machine", "category": "Hardware", "quantity": 10, "unit": "pcs", "price": 4500, "cost": 3500, "reorder": 3},
        {"name": "Measuring Tape", "category": "Hardware", "quantity": 45, "unit": "pcs", "price": 250, "cost": 150, "reorder": 15},
    ]
    
    product_ids = []
    for product_data in products_data:
        supplier_id = random.choice(supplier_ids) if supplier_ids else None
        
        product_id = Product.create_product(
            name=product_data["name"],
            description=f"High quality {product_data['name'].lower()}",
            category=product_data["category"],
            quantity=product_data["quantity"],
            unit=product_data["unit"],
            price=product_data["price"],
            cost=product_data["cost"],
            reorder_level=product_data["reorder"],
            supplier_id=supplier_id
        )
        
        if product_id:
            product_ids.append(product_id)
            print(f"✅ Created product: {product_data['name']}")
    
    return product_ids


def seed_database():
    """Seed database with demo data"""
    print("\n🌱 Seeding database with demo data...\n")
    
    # Create demo user
    create_demo_user()
    
    # Create suppliers
    supplier_ids = create_demo_suppliers()
    
    # Create products
    product_ids = create_demo_products(supplier_ids)
    
    print(f"\n✅ Database seeded successfully!")
    print(f"   - 1 demo user (admin/admin123)")
    print(f"   - {len(supplier_ids)} suppliers")
    print(f"   - {len(product_ids)} products")
    print("\n🚀 You can now run the application with: streamlit run app.py\n")


if __name__ == "__main__":
    from config.database import init_db
    
    # Initialize database
    init_db()
    
    # Seed data
    seed_database()
