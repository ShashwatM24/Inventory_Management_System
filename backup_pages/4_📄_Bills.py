"""
Bills Page - Invoice Generation and Management
"""
import streamlit as st
from models.bill import Bill
from models.product import Product
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import os

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Please login first")
    st.stop()

# Add classy sidebar CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"] { background-color: #0f1419; }
        [data-testid="stSidebarNav"] li:first-child a { visibility: hidden; position: relative; }
        [data-testid="stSidebarNav"] li:first-child a::before {
            content: "🏠 Dashboard"; visibility: visible; position: absolute; left: 0; top: 0;
        }
        [data-testid="stSidebarNav"] ul { padding: 0; }
        [data-testid="stSidebarNav"] li {
            background-color: transparent !important;
            border-radius: 8px;
            margin: 3px 8px;
            transition: all 0.2s ease;
        }
        [data-testid="stSidebarNav"] li:hover { background-color: rgba(6, 182, 212, 0.12) !important; }
        [data-testid="stSidebarNav"] li[aria-selected="true"] {
            background: linear-gradient(90deg, rgba(6, 182, 212, 0.2) 0%, rgba(6, 182, 212, 0.05) 100%) !important;
            border-left: 3px solid #06b6d4;
        }
        [data-testid="stSidebarNav"] a { color: #e0e0e0 !important; font-weight: 500; padding: 0.6rem 1rem; }
        [data-testid="stSidebarNav"] a:hover { color: #06b6d4 !important; }
        [data-testid="stSidebarNav"] li[aria-selected="true"] a { color: #06b6d4 !important; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Bills & Invoices")

# Tabs
tab1, tab2 = st.tabs(["➕ Create Bill", "📋 View Bills"])

# Tab 1: Create Bill
with tab1:
    st.subheader("Create New Bill")
    
    # Customer information
    col1, col2 = st.columns(2)
    
    with col1:
        customer_name = st.text_input("Customer Name *", placeholder="Enter customer name")
    
    with col2:
        customer_contact = st.text_input("Customer Contact *", placeholder="Phone number")
    
    st.markdown("---")
    
    # Product selection
    st.subheader("Add Products")
    
    # Initialize cart in session state
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    # Get all products
    products = Product.get_all_products()
    product_options = [f"{p['name']} - {p['sku']} (Stock: {p['quantity']})" for p in products]
    
    if products:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            selected_product = st.selectbox("Select Product", product_options)
        
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)
        
        with col3:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("➕ Add to Cart", use_container_width=True):
                # Extract SKU
                sku = selected_product.split('-')[1].split('(')[0].strip()
                product = Product.get_product_by_sku(sku)
                
                if product:
                    if quantity > product['quantity']:
                        st.error(f"❌ Only {product['quantity']} units available!")
                    else:
                        # Add to cart
                        cart_item = {
                            'product_id': str(product['_id']),
                            'name': product['name'],
                            'sku': product['sku'],
                            'quantity': quantity,
                            'price': product['price'],
                            'total': quantity * product['price']
                        }
                        st.session_state.cart.append(cart_item)
                        st.success(f"✅ Added {quantity} x {product['name']} to cart")
                        st.rerun()
    else:
        st.warning("⚠️ No products available. Please add products first.")
    
    # Display cart
    if st.session_state.cart:
        st.markdown("---")
        st.subheader("🛒 Cart Items")
        
        cart_df = pd.DataFrame([{
            'Product': item['name'],
            'SKU': item['sku'],
            'Quantity': item['quantity'],
            'Price': f"₹{item['price']:,.2f}",
            'Total': f"₹{item['total']:,.2f}"
        } for item in st.session_state.cart])
        
        st.dataframe(cart_df, use_container_width=True, hide_index=True)
        
        # Remove item
        item_to_remove = st.selectbox("Remove Item", 
                                     [f"{item['name']} ({item['sku']})" for item in st.session_state.cart],
                                     key="remove_item")
        if st.button("🗑️ Remove Selected Item"):
            sku_to_remove = item_to_remove.split('(')[1].strip(')')
            st.session_state.cart = [item for item in st.session_state.cart if item['sku'] != sku_to_remove]
            st.rerun()
        
        # Bill summary
        st.markdown("---")
        st.subheader("💰 Bill Summary")
        
        subtotal = sum(item['total'] for item in st.session_state.cart)
        
        col1, col2 = st.columns(2)
        
        with col1:
            tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, max_value=100.0, value=18.0, step=0.1) / 100
            discount = st.number_input("Discount (₹)", min_value=0.0, value=0.0, step=0.01)
        
        with col2:
            tax = subtotal * tax_rate
            total = subtotal + tax - discount
            
            st.metric("Subtotal", f"₹{subtotal:,.2f}")
            st.metric("Tax", f"₹{tax:,.2f}")
            st.metric("Discount", f"₹{discount:,.2f}")
            st.metric("**Total**", f"**₹{total:,.2f}**")
        
        # Generate bill
        st.markdown("---")
        
        if st.button("📄 Generate Bill", type="primary", use_container_width=True):
            if not customer_name or not customer_contact:
                st.error("❌ Please enter customer name and contact")
            else:
                # Create bill
                bill_id = Bill.create_bill(
                    customer_name=customer_name,
                    customer_contact=customer_contact,
                    items=st.session_state.cart,
                    tax_rate=tax_rate,
                    discount=discount,
                    created_by=st.session_state.user['id']
                )
                
                if bill_id:
                    # Update product quantities
                    for item in st.session_state.cart:
                        Product.update_stock(
                            item['product_id'],
                            -item['quantity'],
                            "sale",
                            f"Sold via bill {Bill.get_bill_by_id(bill_id)['bill_number']}"
                        )
                    
                    bill = Bill.get_bill_by_id(bill_id)
                    st.success(f"✅ Bill generated successfully! Bill Number: {bill['bill_number']}")
                    
                    # Clear cart
                    st.session_state.cart = []
                    
                    # Generate PDF
                    generate_pdf_invoice(bill)
                    
                    st.rerun()
                else:
                    st.error("❌ Failed to generate bill")
    else:
        st.info("🛒 Cart is empty. Add products to create a bill.")

# Tab 2: View Bills
with tab2:
    st.subheader("All Bills")
    
    # Search
    search_term = st.text_input("🔍 Search Bills", placeholder="Search by customer name, bill number, or contact")
    
    # Get bills
    if search_term:
        bills = Bill.search_bills(search_term)
    else:
        bills = Bill.get_all_bills(limit=100)
    
    if bills:
        st.write(f"Found {len(bills)} bill(s)")
        
        # Display bills
        for bill in bills:
            with st.expander(f"📄 {bill['bill_number']} - {bill['customer_name']} - ₹{bill['total']:,.2f}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Customer:** {bill['customer_name']}")
                    st.write(f"**Contact:** {bill['customer_contact']}")
                    st.write(f"**Date:** {bill['created_at'].strftime('%Y-%m-%d %H:%M')}")
                
                with col2:
                    st.write(f"**Subtotal:** ₹{bill['subtotal']:,.2f}")
                    st.write(f"**Tax:** ₹{bill['tax']:,.2f}")
                    st.write(f"**Discount:** ₹{bill['discount']:,.2f}")
                    st.write(f"**Total:** ₹{bill['total']:,.2f}")
                
                # Items
                st.markdown("**Items:**")
                items_df = pd.DataFrame([{
                    'Product': item['name'],
                    'Quantity': item['quantity'],
                    'Price': f"₹{item['price']:,.2f}",
                    'Total': f"₹{item['total']:,.2f}"
                } for item in bill['items']])
                
                st.dataframe(items_df, use_container_width=True, hide_index=True)
                
                # Download PDF
                if st.button(f"📥 Download PDF", key=f"download_{bill['_id']}"):
                    generate_pdf_invoice(bill)
    else:
        st.info("No bills found")


def generate_pdf_invoice(bill):
    """Generate PDF invoice for a bill"""
    try:
        # Create bills directory if it doesn't exist
        os.makedirs("bills", exist_ok=True)
        
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 10, "INVOICE", ln=True, align="C")
        pdf.ln(5)
        
        # Bill details
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Bill Number: {bill['bill_number']}", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 8, f"Date: {bill['created_at'].strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.ln(5)
        
        # Customer details
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Customer Details:", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 8, f"Name: {bill['customer_name']}", ln=True)
        pdf.cell(0, 8, f"Contact: {bill['customer_contact']}", ln=True)
        pdf.ln(5)
        
        # Items table
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Items:", ln=True)
        
        # Table header
        pdf.set_font("Arial", "B", 10)
        pdf.cell(80, 8, "Product", border=1)
        pdf.cell(30, 8, "Quantity", border=1)
        pdf.cell(40, 8, "Price", border=1)
        pdf.cell(40, 8, "Total", border=1)
        pdf.ln()
        
        # Table rows
        pdf.set_font("Arial", "", 10)
        for item in bill['items']:
            pdf.cell(80, 8, item['name'][:30], border=1)
            pdf.cell(30, 8, str(item['quantity']), border=1)
            pdf.cell(40, 8, f"Rs. {item['price']:,.2f}", border=1)
            pdf.cell(40, 8, f"Rs. {item['total']:,.2f}", border=1)
            pdf.ln()
        
        pdf.ln(5)
        
        # Totals
        pdf.set_font("Arial", "B", 10)
        pdf.cell(150, 8, "Subtotal:", align="R")
        pdf.cell(40, 8, f"Rs. {bill['subtotal']:,.2f}", ln=True, align="R")
        
        pdf.cell(150, 8, f"Tax ({bill['tax_rate']*100:.1f}%):", align="R")
        pdf.cell(40, 8, f"Rs. {bill['tax']:,.2f}", ln=True, align="R")
        
        pdf.cell(150, 8, "Discount:", align="R")
        pdf.cell(40, 8, f"Rs. {bill['discount']:,.2f}", ln=True, align="R")
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(150, 10, "TOTAL:", align="R")
        pdf.cell(40, 10, f"Rs. {bill['total']:,.2f}", ln=True, align="R")
        
        # Save PDF
        filename = f"bills/{bill['bill_number']}.pdf"
        pdf.output(filename)
        
        # Provide download
        with open(filename, "rb") as f:
            st.download_button(
                label="📥 Download PDF",
                data=f,
                file_name=f"{bill['bill_number']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        st.success(f"✅ PDF generated: {filename}")
    
    except Exception as e:
        st.error(f"❌ Failed to generate PDF: {e}")
