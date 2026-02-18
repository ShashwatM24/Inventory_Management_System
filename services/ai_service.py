"""
AI Service - Google Gemini Integration with Scaledown API
"""
import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from models.product import Product
from models.sales_order import SalesOrder
from models.purchase_order import PurchaseOrder
from models.supplier import Supplier
from models.supplier import Supplier
from models.invoice import Invoice
from utils.analytics import get_sales_analytics_summary
import re

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY")

# Initialize Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def get_full_business_context():
    """
    Fetch comprehensive business data for AI context
    Aggregates Inventory, Sales, Procurement, and Financials
    """
    try:
        # Fetch Data
        products = Product.get_all_products()
        low_stock = Product.get_low_stock_items()
        low_stock = Product.get_low_stock_items()
        sales_orders = SalesOrder.get_all_orders(limit=100) # Fetch more for analytics
        purchase_orders = PurchaseOrder.get_all_pos(limit=10)
        purchase_orders = PurchaseOrder.get_all_pos(limit=10)
        suppliers = Supplier.get_all_suppliers()
        invoices = Invoice.get_all_invoices(limit=10)
        
        context = "=== 🏢 VAULTLY BUSINESS INTELLIGENCE CONTEXT ===\n\n"
        
        # 1. INVENTORY STATUS
        context += f"--- 📦 INVENTORY SUMMARY ---\n"
        context += f"Total SKU Count: {len(products)}\n"
        context += f"Low Stock Alerts: {len(low_stock)} items\n"
        if low_stock:
            context += "⚠️ CRITICAL LOW STOCK:\n"
            for item in low_stock:
                name = item.get('name', 'Unknown')
                qty = item.get('quantity', item.get('stock', 0))
                unit = item.get('unit', 'units')
                reorder = item.get('reorder_level', 0)
                context += f"- {name} (Qty: {qty} {unit}, Reorder Lvl: {reorder})\n"
        context += "\n"

        # 2. PRODUCT CATALOG (Top 30 by default to save tokens)
        context += f"--- 📋 PRODUCT CATALOG (Sample) ---\n"
        for p in products[:30]:
            pid = str(p.get('_id', 'N/A'))
            name = p.get('name', 'Unknown')
            sku = p.get('sku', 'N/A')
            price = p.get('price', 0.0)
            cost = p.get('cost', 0.0)
            stock = p.get('quantity', p.get('stock', 0))
            context += f"- ID: {pid} | {name} (SKU: {sku}, Price: ₹{price}, Cost: ₹{cost}, Stock: {stock})\n"
        context += "\n"

        # 3. SALES & ORDERS
        context += f"--- 🛒 RECENT SALES ORDERS (Last 10) ---\n"
        for so in sales_orders[:10]:
            order_num = so.get('order_number', 'N/A')
            cust_name = so.get('customer_name', 'Unknown')
            total = so.get('total_amount', 0.0)
            status = so.get('status', 'Unknown')
            date = so.get('order_date')
            date_str = date.strftime('%Y-%m-%d') if date else 'N/A'
            context += f"- Order {order_num} | {cust_name} | ₹{total:,.2f} | Status: {status} | Date: {date_str}\n"
            
            # Add Line Items
            items = so.get('items', [])
            if items:
                item_details = []
                for item in items:
                    i_name = item.get('name', 'Unknown')
                    i_qty = item.get('quantity', 0)
                    item_details.append(f"{i_name} (Qty: {i_qty})")
                context += f"  Items: {', '.join(item_details)}\n"
        context += "\n"

        # ... (Rest of context generation remains same)

        # 4. SALES ANALYTICS
        analytics = get_sales_analytics_summary(sales_orders)
        context += f"\n{analytics}\n"

        return context
    
    except Exception as e:
        return f"Error assembling business context: {e}"


def compress_with_scaledown(text):
    # ... (remains same)
    if not SCALEDOWN_API_KEY:
        return text, None
    
    try:
        url = "https://api.scaledown.ai/v1/compress"
        headers = {
            "Authorization": f"Bearer {SCALEDOWN_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "compression_level": "medium"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            compressed_text = result.get('compressed_text', text)
            stats = {
                'original_tokens': result.get('original_tokens', len(text.split())),
                'compressed_tokens': result.get('compressed_tokens', len(compressed_text.split())),
                'compression_ratio': result.get('compression_ratio', 1.0)
            }
            return compressed_text, stats
        else:
            return text, None
    
    except Exception as e:
        print(f"Scaledown compression failed: {e}")
        return text, None


def get_system_prompt(context):
    """Generate the agentic system prompt"""
    return f"""You are 'Vaultly AI', an intelligent and proactive Operations Manager for this inventory system.
    
📊 **YOUR ROLE:**
You are not just a database reader; you are a strategic partner. You analyze the business data to provide actionable insights, answer complex queries, and help the user manage their inventory effectively. You allow the user to effectively "chat" with their data.

🧠 **INTELLIGENCE GUIDELINES:**
1.  **Deep Understanding:** If a user asks "What did we sell last?", look at the most recent Sales Order.
2.  **Proactive Alerts:** If you see "Low Stock", suggest creating a Purchase Order.
3.  **Financial Awareness:** Connect dots between Sales and Invoices.
4.  **Natural Conversation:** Speak like a helpful, professional colleague.
5.  **Visuals & Actions:** You can output JSON to create charts OR perform actions.

**JSON FORMAT FOR CHARTS:**
```json
{{
  "type": "pie", 
  "data": {{ "Label1": 10, "Label2": 20 }},
  "title": "Chart Title"
}}
```

**JSON FORMAT FOR ACTIONS:**
If the user wants to perform an action (like creating a Purchase Order), return this JSON:
```json
{{
  "type": "action",
  "action": "create_po",
  "data": {{
    "supplier_name": "Supplier Name",  // Use "UNKNOWN_SUPPLIER" if valid supplier is not specified
    ]
  }}
}}
```

**JSON FORMAT FOR DRAFTING EMAILS:**
If the user wants to draft an email to a supplier or customer, return this JSON:
```json
{{
  "type": "action",
  "action": "draft_email",
  "data": {{
    "recipient": "supplier@example.com",
    "subject": "Purchase Order Request",
    "body": "Dear Supplier, \n\nI would like to place an order for..."
  }}
}}
```

💡 **EXAMPLE INTERACTIONS:**
- User: "Order 50 Keyboards from TechSupply."
  You: "I've drafted a Purchase Order for 50 Keyboards.
  ```json
  {{
    "type": "action",
    "action": "create_po",
    "data": {{
      "supplier_name": "TechSupply",
      "items": [ {{ "product_id": "65c...", "name": "Keyboard", "quantity": 50, "price": 500 }} ]
    }}
  }}
  ```

📂 **LIVE BUSINESS INTELLIGENCE:**
{context}

Answer the user's request based *strictly* on this data."""


def chat_with_ai(user_message, chat_history=None, image_data=None):
    """
    Chat with Gemini AI (gemini-pro) with full business context
    """
    if not GEMINI_API_KEY:
        return "❌ Gemini API key not configured. Please add GEMINI_API_KEY to your .env file.", None
    
    try:
        # Get full business context
        context = get_full_business_context()
        
        # --- SMART SEARCH INJECTION ---
        if user_message:
            # Check for explicit search keywords or just assume if it looks like a query
            # We'll use a simple regex to extract potential search terms if it starts with find/search/etc
            # But the Product.search_products is robust, so we can also try to run it on key nouns.
            # For simplicity and robust RAG, we will try to find products matching the user message if it's short, or specific keywords.
            
            search_match = re.search(r"(?:find|search|where is|looking for|show me)\s+(.*)", user_message, re.IGNORECASE)
            search_term = search_match.group(1).strip() if search_match else user_message
            
            # Run search if it looks like a product query (simple heuristic)
            if len(search_term) > 2 and len(search_term) < 50:
                 results = Product.search_products(search_term)
                 if results:
                    context += f"\n\n--- 🔍 SMART SEARCH RESULTS ('{search_term}') ---\n"
                    # Filter out products already in top 30 to avoid duplicates? 
                    # For now just append, context window can handle small dupes.
                    for p in results[:10]:
                        pid = str(p.get('_id', 'N/A'))
                        name = p.get('name', 'Unknown')
                        sku = p.get('sku', 'N/A')
                        price = p.get('price', 0.0)
                        stock = p.get('quantity', p.get('stock', 0))
                        context += f"- ID: {pid} | {name} (SKU: {sku}, Price: ₹{price}, Stock: {stock})\n"
        # ------------------------------
        
        # Compress context
        compressed_context, stats = compress_with_scaledown(context)
        
        # Build prompt
        system_prompt = get_system_prompt(compressed_context)
        
        # Initialize model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        full_prompt = f"{system_prompt}\n\nUSER REQUEST: {user_message}\n\nOPERATIONS MANAGER RESPONSE:"
        
        content = [full_prompt]
        if image_data:
             content.append(image_data)
        
        response = model.generate_content(content)
        
        return response.text, stats
    
    except Exception as e:
        return f"❌ Error: {str(e)}", None


def stream_ai_response(user_message, image_data=None):
    """
    Stream AI response for real-time display
    """
    if not GEMINI_API_KEY:
        yield "❌ Gemini API key not configured. Please add GEMINI_API_KEY to your .env file."
        return
    
    try:
        context = get_full_business_context()
        
        # --- SMART SEARCH INJECTION ---
        if user_message:
            search_match = re.search(r"(?:find|search|where is|looking for|show me)\s+(.*)", user_message, re.IGNORECASE)
            search_term = search_match.group(1).strip() if search_match else user_message
            
            if len(search_term) > 2 and len(search_term) < 50:
                 results = Product.search_products(search_term)
                 if results:
                    context += f"\n\n--- 🔍 SMART SEARCH RESULTS ('{search_term}') ---\n"
                    for p in results[:10]:
                        pid = str(p.get('_id', 'N/A'))
                        name = p.get('name', 'Unknown')
                        sku = p.get('sku', 'N/A')
                        price = p.get('price', 0.0)
                        stock = p.get('quantity', p.get('stock', 0))
                        context += f"- ID: {pid} | {name} (SKU: {sku}, Price: ₹{price}, Stock: {stock})\n"
        # ------------------------------

        compressed_context, stats = compress_with_scaledown(context)
        system_prompt = get_system_prompt(compressed_context)
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        full_prompt = f"{system_prompt}\n\nUSER REQUEST: {user_message}\n\nOPERATIONS MANAGER RESPONSE:"
        
        content = [full_prompt]
        if image_data:
             content.append(image_data)
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
        
        response = model.generate_content(content, stream=True, safety_settings=safety_settings)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
    
    except Exception as e:
        yield f"❌ Error: {str(e)}"
