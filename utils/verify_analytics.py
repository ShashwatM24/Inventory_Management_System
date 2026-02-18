
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.analytics import generate_demand_forecast
from datetime import datetime

# Dummy Data
mock_products = [
    {'_id': '1', 'name': 'Widget A', 'stock': 10},
    {'_id': '2', 'name': 'Widget B', 'stock': 5}
]

mock_sales = [
    {'order_date': datetime.now(), 'items': [{'product_id': '1', 'quantity': 5}]},
    {'order_date': datetime.now(), 'items': [{'product_id': '1', 'quantity': 3}]},
    {'order_date': datetime.now(), 'items': [{'product_id': '2', 'quantity': 10}]}
]

print("Testing Demand Forecast...")
forecast = generate_demand_forecast(mock_sales, mock_products)
print("\n--- Generated Forecast ---")
print(forecast)

if "Widget A" in forecast and "Est. Need: 8" in forecast:
    print("\nSUCCESS: Forecast calculation looks correct (5+3=8 for Widget A).")
else:
    print("\nFAIL: Forecast output unexpected.")
