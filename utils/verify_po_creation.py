
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.purchase_order import PurchaseOrder
from datetime import datetime
from bson import ObjectId

# Test Data
po_number = "PO-TEST-123"
supplier_name = "Test Supplier"
items = [
    {
        "product_id": str(ObjectId()),
        "name": "Test Item",
        "quantity": 10,
        "price": 100, 
        "total": 1000
    }
]

print(f"Creating Purchase Order {po_number}...")
po_id = PurchaseOrder.create_po(
    po_number=po_number,
    supplier_id=None,
    supplier_name=supplier_name,
    order_date=datetime.now(),
    expected_delivery=None,
    items=items,
    status="Draft",
    notes="Verification Test"
)

if po_id:
    print(f"SUCCESS: Created PO with ID: {po_id}")
    # Cleanup (Optional, but good practice if not using mock DB)
    # delete_po(po_id) - not implemented in model, so we'll just leave it or manually cleanup.
else:
    print("FAIL: PO Creation returned None")
