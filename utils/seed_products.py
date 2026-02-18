"""
Seed Data Script - Populate Database with 100 Sample Products
Run this script to add diverse sample products to your inventory
"""
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.product import Product
from config.database import init_db
import random

# Initialize database
init_db()

# Sample data for 100 diverse products
products_data = [
    # Electronics (20 items)
    {"name": "Dell XPS 15 Laptop", "category": "Electronics", "price": 125000, "cost": 95000, "stock": 15, "unit": "pcs", "reorder_level": 5, "description": "15.6\" 4K display, i7 processor, 16GB RAM"},
    {"name": "MacBook Pro 14\"", "category": "Electronics", "price": 189000, "cost": 145000, "stock": 8, "unit": "pcs", "reorder_level": 3, "description": "M2 Pro chip, 16GB RAM, 512GB SSD"},
    {"name": "HP LaserJet Printer", "category": "Electronics", "price": 18500, "cost": 14000, "stock": 25, "unit": "pcs", "reorder_level": 10, "description": "Wireless laser printer with duplex"},
    {"name": "Samsung 27\" Monitor", "category": "Electronics", "price": 22000, "cost": 16500, "stock": 30, "unit": "pcs", "reorder_level": 8, "description": "4K UHD, 60Hz, IPS panel"},
    {"name": "Logitech MX Master 3", "category": "Electronics", "price": 8500, "cost": 6200, "stock": 50, "unit": "pcs", "reorder_level": 15, "description": "Wireless mouse with ergonomic design"},
    {"name": "iPhone 15 Pro", "category": "Electronics", "price": 134900, "cost": 105000, "stock": 12, "unit": "pcs", "reorder_level": 5, "description": "256GB, Titanium finish"},
    {"name": "Samsung Galaxy S24", "category": "Electronics", "price": 79999, "cost": 62000, "stock": 18, "unit": "pcs", "reorder_level": 6, "description": "128GB, AI features"},
    {"name": "iPad Air 11\"", "category": "Electronics", "price": 59900, "cost": 46000, "stock": 20, "unit": "pcs", "reorder_level": 7, "description": "M2 chip, 128GB storage"},
    {"name": "Sony WH-1000XM5", "category": "Electronics", "price": 29990, "cost": 22000, "stock": 35, "unit": "pcs", "reorder_level": 12, "description": "Noise cancelling headphones"},
    {"name": "Canon EOS R6", "category": "Electronics", "price": 215000, "cost": 175000, "stock": 5, "unit": "pcs", "reorder_level": 2, "description": "Full-frame mirrorless camera"},
    {"name": "GoPro Hero 12", "category": "Electronics", "price": 44999, "cost": 35000, "stock": 15, "unit": "pcs", "reorder_level": 5, "description": "Action camera with 5.3K video"},
    {"name": "DJI Mini 3 Pro", "category": "Electronics", "price": 59999, "cost": 47000, "stock": 8, "unit": "pcs", "reorder_level": 3, "description": "Foldable drone with 4K camera"},
    {"name": "Kindle Paperwhite", "category": "Electronics", "price": 13999, "cost": 10500, "stock": 40, "unit": "pcs", "reorder_level": 15, "description": "Waterproof e-reader, 8GB"},
    {"name": "Apple Watch Series 9", "category": "Electronics", "price": 41900, "cost": 32000, "stock": 22, "unit": "pcs", "reorder_level": 8, "description": "GPS, 41mm, Aluminum"},
    {"name": "JBL Flip 6", "category": "Electronics", "price": 12999, "cost": 9500, "stock": 45, "unit": "pcs", "reorder_level": 15, "description": "Portable Bluetooth speaker"},
    {"name": "Anker PowerCore 20000", "category": "Electronics", "price": 3999, "cost": 2800, "stock": 60, "unit": "pcs", "reorder_level": 20, "description": "High-capacity power bank"},
    {"name": "SanDisk 1TB SSD", "category": "Electronics", "price": 8999, "cost": 6500, "stock": 50, "unit": "pcs", "reorder_level": 18, "description": "Portable external SSD"},
    {"name": "TP-Link WiFi Router", "category": "Electronics", "price": 4999, "cost": 3500, "stock": 35, "unit": "pcs", "reorder_level": 12, "description": "AC1900 dual-band router"},
    {"name": "Webcam Logitech C920", "category": "Electronics", "price": 7999, "cost": 5800, "stock": 28, "unit": "pcs", "reorder_level": 10, "description": "1080p HD webcam"},
    {"name": "Blue Yeti Microphone", "category": "Electronics", "price": 12999, "cost": 9500, "stock": 18, "unit": "pcs", "reorder_level": 6, "description": "USB condenser microphone"},
    
    # Furniture (15 items)
    {"name": "Executive Office Chair", "category": "Furniture", "price": 18500, "cost": 13000, "stock": 25, "unit": "pcs", "reorder_level": 8, "description": "Ergonomic leather chair with lumbar support"},
    {"name": "Standing Desk Adjustable", "category": "Furniture", "price": 32000, "cost": 24000, "stock": 12, "unit": "pcs", "reorder_level": 5, "description": "Electric height adjustable desk"},
    {"name": "Conference Table 8-Seater", "category": "Furniture", "price": 45000, "cost": 32000, "stock": 8, "unit": "pcs", "reorder_level": 3, "description": "Wooden conference table"},
    {"name": "Filing Cabinet 4-Drawer", "category": "Furniture", "price": 12500, "cost": 9000, "stock": 20, "unit": "pcs", "reorder_level": 7, "description": "Metal filing cabinet with lock"},
    {"name": "Bookshelf 5-Tier", "category": "Furniture", "price": 8999, "cost": 6500, "stock": 15, "unit": "pcs", "reorder_level": 5, "description": "Wooden bookshelf, walnut finish"},
    {"name": "Reception Desk", "category": "Furniture", "price": 55000, "cost": 40000, "stock": 5, "unit": "pcs", "reorder_level": 2, "description": "Modern reception counter"},
    {"name": "Visitor Chair Set (2)", "category": "Furniture", "price": 9500, "cost": 7000, "stock": 30, "unit": "sets", "reorder_level": 10, "description": "Cushioned visitor chairs"},
    {"name": "Computer Desk", "category": "Furniture", "price": 14999, "cost": 11000, "stock": 18, "unit": "pcs", "reorder_level": 6, "description": "L-shaped computer desk"},
    {"name": "Storage Cabinet", "category": "Furniture", "price": 16500, "cost": 12000, "stock": 12, "unit": "pcs", "reorder_level": 5, "description": "Office storage cabinet with doors"},
    {"name": "Sofa 3-Seater", "category": "Furniture", "price": 38000, "cost": 28000, "stock": 8, "unit": "pcs", "reorder_level": 3, "description": "Fabric sofa for waiting area"},
    {"name": "Coffee Table", "category": "Furniture", "price": 7500, "cost": 5500, "stock": 15, "unit": "pcs", "reorder_level": 5, "description": "Glass top coffee table"},
    {"name": "Whiteboard 6x4 ft", "category": "Furniture", "price": 5500, "cost": 4000, "stock": 22, "unit": "pcs", "reorder_level": 8, "description": "Magnetic whiteboard with stand"},
    {"name": "Partition Panel", "category": "Furniture", "price": 8500, "cost": 6200, "stock": 25, "unit": "pcs", "reorder_level": 10, "description": "Office cubicle partition"},
    {"name": "Ergonomic Footrest", "category": "Furniture", "price": 2500, "cost": 1800, "stock": 40, "unit": "pcs", "reorder_level": 15, "description": "Adjustable footrest"},
    {"name": "Monitor Stand Dual", "category": "Furniture", "price": 4999, "cost": 3500, "stock": 30, "unit": "pcs", "reorder_level": 10, "description": "Dual monitor arm stand"},
    
    # Stationery (20 items)
    {"name": "A4 Paper Ream (500 sheets)", "category": "Stationery", "price": 350, "cost": 250, "stock": 200, "unit": "reams", "reorder_level": 50, "description": "Premium white A4 paper"},
    {"name": "Ballpoint Pen Blue (Box of 50)", "category": "Stationery", "price": 500, "cost": 350, "stock": 100, "unit": "boxes", "reorder_level": 30, "description": "Smooth writing pens"},
    {"name": "Stapler Heavy Duty", "category": "Stationery", "price": 450, "cost": 320, "stock": 75, "unit": "pcs", "reorder_level": 25, "description": "Metal stapler, 50 sheet capacity"},
    {"name": "Staples Box (1000 pcs)", "category": "Stationery", "price": 80, "cost": 55, "stock": 150, "unit": "boxes", "reorder_level": 50, "description": "Standard staples"},
    {"name": "File Folders (Pack of 25)", "category": "Stationery", "price": 250, "cost": 180, "stock": 120, "unit": "packs", "reorder_level": 40, "description": "Manila file folders"},
    {"name": "Sticky Notes 3x3 (Pack of 12)", "category": "Stationery", "price": 180, "cost": 130, "stock": 90, "unit": "packs", "reorder_level": 30, "description": "Assorted color sticky notes"},
    {"name": "Highlighter Set (4 colors)", "category": "Stationery", "price": 120, "cost": 85, "stock": 80, "unit": "sets", "reorder_level": 25, "description": "Fluorescent highlighters"},
    {"name": "Notebook A5 Ruled", "category": "Stationery", "price": 85, "cost": 60, "stock": 150, "unit": "pcs", "reorder_level": 50, "description": "200 pages spiral notebook"},
    {"name": "Permanent Marker Black", "category": "Stationery", "price": 45, "cost": 30, "stock": 100, "unit": "pcs", "reorder_level": 35, "description": "Waterproof marker"},
    {"name": "Paper Clips Box (100 pcs)", "category": "Stationery", "price": 35, "cost": 25, "stock": 120, "unit": "boxes", "reorder_level": 40, "description": "Metal paper clips"},
    {"name": "Binder Clips Assorted", "category": "Stationery", "price": 150, "cost": 105, "stock": 85, "unit": "boxes", "reorder_level": 30, "description": "Various sizes binder clips"},
    {"name": "Correction Tape", "category": "Stationery", "price": 55, "cost": 38, "stock": 95, "unit": "pcs", "reorder_level": 30, "description": "White correction tape"},
    {"name": "Scissors 8 inch", "category": "Stationery", "price": 95, "cost": 65, "stock": 70, "unit": "pcs", "reorder_level": 25, "description": "Stainless steel scissors"},
    {"name": "Glue Stick 20g", "category": "Stationery", "price": 40, "cost": 28, "stock": 110, "unit": "pcs", "reorder_level": 40, "description": "Non-toxic glue stick"},
    {"name": "Envelope A4 (Pack of 50)", "category": "Stationery", "price": 200, "cost": 140, "stock": 80, "unit": "packs", "reorder_level": 25, "description": "White envelopes"},
    {"name": "Ruler 30cm Steel", "category": "Stationery", "price": 65, "cost": 45, "stock": 90, "unit": "pcs", "reorder_level": 30, "description": "Stainless steel ruler"},
    {"name": "Eraser White (Pack of 10)", "category": "Stationery", "price": 50, "cost": 35, "stock": 100, "unit": "packs", "reorder_level": 35, "description": "Soft erasers"},
    {"name": "Pencil HB (Box of 12)", "category": "Stationery", "price": 120, "cost": 85, "stock": 75, "unit": "boxes", "reorder_level": 25, "description": "Graphite pencils"},
    {"name": "Calculator Desktop", "category": "Stationery", "price": 550, "cost": 400, "stock": 45, "unit": "pcs", "reorder_level": 15, "description": "12-digit calculator"},
    {"name": "Desk Organizer", "category": "Stationery", "price": 450, "cost": 320, "stock": 50, "unit": "pcs", "reorder_level": 18, "description": "Multi-compartment organizer"},
    
    # Cleaning Supplies (10 items)
    {"name": "Floor Cleaner 5L", "category": "Cleaning", "price": 450, "cost": 320, "stock": 60, "unit": "bottles", "reorder_level": 20, "description": "Multi-surface floor cleaner"},
    {"name": "Disinfectant Spray 500ml", "category": "Cleaning", "price": 280, "cost": 200, "stock": 80, "unit": "bottles", "reorder_level": 25, "description": "Antibacterial spray"},
    {"name": "Toilet Cleaner 1L", "category": "Cleaning", "price": 180, "cost": 130, "stock": 70, "unit": "bottles", "reorder_level": 25, "description": "Thick toilet cleaner"},
    {"name": "Glass Cleaner 500ml", "category": "Cleaning", "price": 220, "cost": 160, "stock": 65, "unit": "bottles", "reorder_level": 20, "description": "Streak-free glass cleaner"},
    {"name": "Mop with Bucket", "category": "Cleaning", "price": 850, "cost": 620, "stock": 25, "unit": "sets", "reorder_level": 8, "description": "Spin mop with bucket"},
    {"name": "Broom with Dustpan", "category": "Cleaning", "price": 350, "cost": 250, "stock": 40, "unit": "sets", "reorder_level": 12, "description": "Soft bristle broom set"},
    {"name": "Garbage Bags 30L (Pack of 30)", "category": "Cleaning", "price": 180, "cost": 130, "stock": 90, "unit": "packs", "reorder_level": 30, "description": "Heavy duty garbage bags"},
    {"name": "Microfiber Cloth (Pack of 5)", "category": "Cleaning", "price": 250, "cost": 180, "stock": 55, "unit": "packs", "reorder_level": 18, "description": "Reusable cleaning cloths"},
    {"name": "Hand Soap Liquid 5L", "category": "Cleaning", "price": 550, "cost": 400, "stock": 45, "unit": "bottles", "reorder_level": 15, "description": "Antibacterial hand wash"},
    {"name": "Paper Towel Roll (Pack of 6)", "category": "Cleaning", "price": 320, "cost": 230, "stock": 70, "unit": "packs", "reorder_level": 25, "description": "Absorbent paper towels"},
    
    # Pantry/Beverages (15 items)
    {"name": "Coffee Beans 1kg", "category": "Pantry", "price": 1200, "cost": 900, "stock": 35, "unit": "kg", "reorder_level": 12, "description": "Premium arabica coffee beans"},
    {"name": "Tea Bags (Pack of 100)", "category": "Pantry", "price": 350, "cost": 250, "stock": 60, "unit": "packs", "reorder_level": 20, "description": "Assorted tea flavors"},
    {"name": "Sugar 5kg", "category": "Pantry", "price": 280, "cost": 200, "stock": 50, "unit": "bags", "reorder_level": 15, "description": "White refined sugar"},
    {"name": "Milk Powder 1kg", "category": "Pantry", "price": 550, "cost": 400, "stock": 40, "unit": "packs", "reorder_level": 15, "description": "Full cream milk powder"},
    {"name": "Biscuits Assorted (Pack of 12)", "category": "Pantry", "price": 480, "cost": 350, "stock": 55, "unit": "packs", "reorder_level": 18, "description": "Mixed biscuit varieties"},
    {"name": "Instant Noodles (Box of 30)", "category": "Pantry", "price": 450, "cost": 320, "stock": 45, "unit": "boxes", "reorder_level": 15, "description": "Quick meal noodles"},
    {"name": "Bottled Water 1L (Pack of 12)", "category": "Pantry", "price": 240, "cost": 170, "stock": 80, "unit": "packs", "reorder_level": 25, "description": "Mineral water bottles"},
    {"name": "Soft Drinks Cans (Pack of 24)", "category": "Pantry", "price": 720, "cost": 520, "stock": 50, "unit": "packs", "reorder_level": 18, "description": "Assorted soda cans"},
    {"name": "Chips Variety Pack (Box of 20)", "category": "Pantry", "price": 600, "cost": 450, "stock": 40, "unit": "boxes", "reorder_level": 15, "description": "Mixed flavor chips"},
    {"name": "Disposable Cups 200ml (Pack of 100)", "category": "Pantry", "price": 180, "cost": 130, "stock": 75, "unit": "packs", "reorder_level": 25, "description": "Paper cups"},
    {"name": "Disposable Plates (Pack of 50)", "category": "Pantry", "price": 220, "cost": 160, "stock": 60, "unit": "packs", "reorder_level": 20, "description": "Eco-friendly plates"},
    {"name": "Napkins (Pack of 100)", "category": "Pantry", "price": 120, "cost": 85, "stock": 90, "unit": "packs", "reorder_level": 30, "description": "Tissue napkins"},
    {"name": "Salt 1kg", "category": "Pantry", "price": 45, "cost": 30, "stock": 70, "unit": "packs", "reorder_level": 25, "description": "Iodized table salt"},
    {"name": "Cooking Oil 5L", "category": "Pantry", "price": 850, "cost": 620, "stock": 30, "unit": "bottles", "reorder_level": 10, "description": "Refined vegetable oil"},
    {"name": "Spices Set (10 varieties)", "category": "Pantry", "price": 650, "cost": 480, "stock": 25, "unit": "sets", "reorder_level": 8, "description": "Common cooking spices"},
    
    # Safety Equipment (10 items)
    {"name": "Fire Extinguisher 2kg", "category": "Safety", "price": 1200, "cost": 900, "stock": 20, "unit": "pcs", "reorder_level": 8, "description": "ABC type fire extinguisher"},
    {"name": "First Aid Kit", "category": "Safety", "price": 850, "cost": 620, "stock": 30, "unit": "kits", "reorder_level": 10, "description": "Complete first aid kit"},
    {"name": "Safety Helmet", "category": "Safety", "price": 450, "cost": 320, "stock": 40, "unit": "pcs", "reorder_level": 15, "description": "Industrial safety helmet"},
    {"name": "Safety Goggles", "category": "Safety", "price": 280, "cost": 200, "stock": 50, "unit": "pcs", "reorder_level": 18, "description": "Protective eyewear"},
    {"name": "Face Masks (Box of 50)", "category": "Safety", "price": 350, "cost": 250, "stock": 60, "unit": "boxes", "reorder_level": 20, "description": "3-ply disposable masks"},
    {"name": "Hand Sanitizer 500ml", "category": "Safety", "price": 220, "cost": 160, "stock": 70, "unit": "bottles", "reorder_level": 25, "description": "70% alcohol sanitizer"},
    {"name": "Safety Gloves (Pair)", "category": "Safety", "price": 180, "cost": 130, "stock": 80, "unit": "pairs", "reorder_level": 30, "description": "Cut-resistant gloves"},
    {"name": "Reflective Vest", "category": "Safety", "price": 320, "cost": 230, "stock": 35, "unit": "pcs", "reorder_level": 12, "description": "High-visibility vest"},
    {"name": "Emergency Exit Sign", "category": "Safety", "price": 650, "cost": 480, "stock": 25, "unit": "pcs", "reorder_level": 8, "description": "LED exit signage"},
    {"name": "Smoke Detector", "category": "Safety", "price": 1100, "cost": 850, "stock": 18, "unit": "pcs", "reorder_level": 6, "description": "Battery-powered smoke alarm"},
    
    # Miscellaneous (10 items)
    {"name": "Wall Clock 12 inch", "category": "Miscellaneous", "price": 650, "cost": 480, "stock": 30, "unit": "pcs", "reorder_level": 10, "description": "Analog wall clock"},
    {"name": "Desk Lamp LED", "category": "Miscellaneous", "price": 1200, "cost": 900, "stock": 25, "unit": "pcs", "reorder_level": 8, "description": "Adjustable LED desk lamp"},
    {"name": "Extension Cord 5m", "category": "Miscellaneous", "price": 450, "cost": 320, "stock": 40, "unit": "pcs", "reorder_level": 15, "description": "4-socket extension cord"},
    {"name": "Umbrella Stand", "category": "Miscellaneous", "price": 850, "cost": 620, "stock": 15, "unit": "pcs", "reorder_level": 5, "description": "Metal umbrella holder"},
    {"name": "Coat Hanger Stand", "category": "Miscellaneous", "price": 1500, "cost": 1100, "stock": 12, "unit": "pcs", "reorder_level": 5, "description": "Wooden coat stand"},
    {"name": "Trash Can 50L", "category": "Miscellaneous", "price": 950, "cost": 700, "stock": 28, "unit": "pcs", "reorder_level": 10, "description": "Pedal bin with lid"},
    {"name": "Notice Board Cork 3x2 ft", "category": "Miscellaneous", "price": 750, "cost": 550, "stock": 20, "unit": "pcs", "reorder_level": 7, "description": "Cork bulletin board"},
    {"name": "Calendar 2024 Wall", "category": "Miscellaneous", "price": 180, "cost": 130, "stock": 50, "unit": "pcs", "reorder_level": 18, "description": "Annual wall calendar"},
    {"name": "Name Plates Desk", "category": "Miscellaneous", "price": 350, "cost": 250, "stock": 45, "unit": "pcs", "reorder_level": 15, "description": "Acrylic desk name plates"},
    {"name": "Key Cabinet 50 Keys", "category": "Miscellaneous", "price": 1800, "cost": 1350, "stock": 10, "unit": "pcs", "reorder_level": 4, "description": "Wall-mounted key cabinet"},
]

def seed_database():
    """Add all sample products to the database"""
    print("🌱 Starting database seeding...")
    print(f"📦 Adding {len(products_data)} products...\n")
    
    added_count = 0
    skipped_count = 0
    
    for idx, product in enumerate(products_data, 1):
        try:
            product_id = Product.create_product(
                name=product["name"],
                description=product["description"],
                category=product["category"],
                quantity=product["stock"],
                unit=product["unit"],
                price=product["price"],
                cost=product["cost"],
                reorder_level=product["reorder_level"]
            )
            
            if product_id:
                added_count += 1
                print(f"✅ [{idx}/{len(products_data)}] Added: {product['name']}")
            else:
                skipped_count += 1
                print(f"⚠️  [{idx}/{len(products_data)}] Skipped (already exists): {product['name']}")
                
        except Exception as e:
            skipped_count += 1
            print(f"❌ [{idx}/{len(products_data)}] Error adding {product['name']}: {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"🎉 Seeding complete!")
    print(f"✅ Successfully added: {added_count} products")
    print(f"⚠️  Skipped: {skipped_count} products")
    print(f"📊 Total in database: {added_count + skipped_count} products")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    seed_database()
