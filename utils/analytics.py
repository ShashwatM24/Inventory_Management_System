
from datetime import datetime, timedelta
import pandas as pd

def generate_demand_forecast(sales_orders, products):
    """
    Generate simple demand forecast based on recent sales.
    Returns a text summary for AI context.
    """
    try:
        if not sales_orders:
            return "No sales data available for forecasting."

        # Flatten sales items
        sales_items = []
        for so in sales_orders:
            order_date = so.get('order_date', datetime.now())
            if isinstance(order_date, str):
                 try:
                     order_date = datetime.strptime(order_date, "%Y-%m-%d")
                 except:
                     order_date = datetime.now()
            
            for item in so.get('items', []):
                sales_items.append({
                    'product_id': str(item.get('product_id')), # Ensure string for grouping
                    'quantity': item.get('quantity', 0),
                    'date': order_date
                })
        
        if not sales_items:
            return "No items sold yet."

        df = pd.DataFrame(sales_items)
        
        # Calculate total sales per product
        # Group by product_id
        summary = df.groupby('product_id')['quantity'].sum().reset_index()
        
        # Calculate time span (days between first and last order or just last 30 days)
        # For simplicity, let's assume the data provided is "Recent" (e.g. last 30 days)
        # In a real app we'd filter by date.
        
        forecast_text = "--- 🔮 DEMAND FORECAST (Next 30 Days) ---\n"
        
        for index, row in summary.iterrows():
            pid = row['product_id']
            qty_sold = row['quantity']
            
            # Find product name
            product_name = "Unknown Product"
            for p in products:
                if str(p.get('_id')) == pid:
                    product_name = p.get('name')
                    break
            
            # Simple Naive Forecast: Assume next month = last month
            # (In a real app, use moving average or linear regression)
            predicted_demand = qty_sold 
            
            forecast_text += f"- {product_name}: Sold {qty_sold} recently. Est. Need: {predicted_demand}\n"
            
        return forecast_text

    except Exception as e:
        return f"Error analyzing data: {e}"

def get_sales_analytics_summary(sales_orders):
    """
    Generate a summary of sales performance.
    """
    try:
        if not sales_orders:
            return "No sales data available."
            
        total_revenue = sum(order.get('total_amount', 0) for order in sales_orders)
        total_orders = len(sales_orders)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Flatten items for product analysis
        all_items = []
        for order in sales_orders:
            for item in order.get('items', []):
                all_items.append({
                    'name': item.get('name', 'Unknown'),
                    'quantity': item.get('quantity', 0),
                    'revenue': item.get('quantity', 0) * item.get('price', 0)
                })
        
        if not all_items:
            return f"Total Revenue: ₹{total_revenue:,.2f} from {total_orders} orders."
            
        df = pd.DataFrame(all_items)
        top_products = df.groupby('name')['quantity'].sum().sort_values(ascending=False).head(5)
        
        summary = "--- 📈 SALES ANALYTICS ---\n"
        summary += f"Total Revenue: ₹{total_revenue:,.2f}\n"
        summary += f"Total Orders: {total_orders}\n"
        summary += f"Avg Order Value: ₹{avg_order_value:,.2f}\n"
        summary += "Top Selling Products:\n"
        
        for name, qty in top_products.items():
            summary += f"- {name}: {qty} units\n"
            
        return summary
        
    except Exception as e:
        return f"Error generating analytics: {e}"
