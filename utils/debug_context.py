
import sys
import os
import traceback

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.product import Product
from models.sales_order import SalesOrder
from models.purchase_order import PurchaseOrder
from models.supplier import Supplier
from models.invoice import Invoice

print("Debugging Business Context Assembly...")

try:
    print("\n1. Fetching Products...")
    products = Product.get_all_products()
    print(f"Fetched {len(products)} products.")
    
    print("\n2. Checking Product 'quantity' fields...")
    for i, p in enumerate(products[:5]): # Check first 5
        print(f"Product {i}: {p.get('name')} keys: {list(p.keys())}")
        if 'quantity' not in p:
            print(f"ERROR: Product {p.get('_id')} missing 'quantity'")

    print("\n3. Fetching Low Stock...")
    low_stock = Product.get_low_stock_items()
    print(f"Fetched {len(low_stock)} low stock items.")
    
    print("\n4. Checking Low Stock 'quantity' fields...")
    for i, item in enumerate(low_stock):
        try:
            val = item['quantity']
        except KeyError:
            print(f"ERROR: Low stock item {item.get('name', 'Unknown')} missing 'quantity'. Keys: {list(item.keys())}")

    print("\n5. Simulating Context Loop (Inventory Summary)...")
    for item in low_stock:
        _ = f"- {item['name']} (Qty: {item['quantity']} {item['unit']}, Reorder Lvl: {item['reorder_level']})\n"

    print("\n6. Simulating Context Loop (Product Catalog)...")
    for p in products[:30]:
        _ = f"- {p['name']} (SKU: {p['sku']}, Price: ₹{p['price']}, Cost: ₹{p.get('cost', 0.0)}, Stock: {p['quantity']})\n"

    print("\nSUCCESS: All checks passed??")

except Exception:
    traceback.print_exc()
