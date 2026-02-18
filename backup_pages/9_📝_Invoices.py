"""
Invoices Page - Generate and manage invoices
"""
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Invoices - Vaultly", page_icon="📝", layout="wide")

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("⚠️ Please login to access this page")
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

st.title("📝 Invoices")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["All Invoices", "Create Invoice", "Invoice Reports"])

with tab1:
    st.subheader("All Invoices")
    st.info("📄 Invoice management system coming soon...")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Invoices", "0", "0")
    with col2:
        st.metric("Paid", "0", "₹0")
    with col3:
        st.metric("Pending", "0", "₹0")
    with col4:
        st.metric("Overdue", "0", "₹0")

with tab2:
    st.subheader("Create New Invoice")
    
    with st.form("create_invoice"):
        col1, col2 = st.columns(2)
        
        with col1:
            invoice_number = st.text_input("Invoice Number", f"INV-{datetime.now().strftime('%Y%m%d')}")
            customer_name = st.text_input("Customer Name")
            invoice_date = st.date_input("Invoice Date", datetime.now())
            
        with col2:
            due_date = st.date_input("Due Date")
            payment_terms = st.selectbox("Payment Terms", ["Net 30", "Net 60", "Due on Receipt", "Custom"])
            status = st.selectbox("Status", ["Draft", "Sent", "Paid", "Overdue"])
        
        items = st.text_area("Items (one per line with price)")
        tax = st.number_input("Tax (%)", min_value=0.0, max_value=100.0, value=0.0)
        notes = st.text_area("Notes")
        
        submit = st.form_submit_button("Create Invoice", use_container_width=True)
        
        if submit:
            st.success("✅ Invoice created successfully!")

with tab3:
    st.subheader("Invoice Reports")
    st.info("📊 Invoice analytics and reports coming soon...")
