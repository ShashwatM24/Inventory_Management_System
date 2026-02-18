
import streamlit as st
from models.product import Product
from models.bill import Bill
import plotly.express as px

def show():
    """Display the dashboard view"""
    st.title("🏠 Welcome to Vaultly")
    st.markdown("### 📊 Dashboard Overview")
    st.info("📍 Navigate to different sections using the sidebar.")
    st.markdown("---")
    
    products = Product.get_all_products()
    low_stock_items = Product.get_low_stock_items()
    bills = Bill.get_all_bills(limit=10)
    
    total_products = len(products)
    low_stock_count = len(low_stock_items)
    total_inventory_value = sum(p.get('stock', 0) * p.get('price', 0) for p in products)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Products", total_products)
    with col2:
        st.metric("Low Stock", low_stock_count)
    with col3:
        st.metric("Inventory Value", f"₹{total_inventory_value:,.2f}")
    with col4:
        st.metric("Total Bills", len(bills))
    
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ Add Product", use_container_width=True):
            st.session_state.current_page = "Inventory"
            st.rerun()
    with col2:
        if st.button("📄 Create Bill", use_container_width=True):
            st.session_state.current_page = "Bills"
            st.rerun()
    with col3:
        if st.button("🤖 AI Chat", use_container_width=True):
            st.session_state.current_page = "AI Chat"
            st.rerun()
    with col4:
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state.current_page = "Reports"
            st.rerun()
