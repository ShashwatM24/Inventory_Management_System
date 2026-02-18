
import streamlit as st
from datetime import datetime

def show():
    """Display the invoices view"""
    st.title("📝 Invoices")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["All Invoices", "Create Invoice", "Invoice Reports"])
    
@st.dialog("Invoice Details")
def show_invoice_details(invoice):
    """Display invoice details in a dialog"""
    st.subheader(f"Invoice: {invoice['invoice_number']}")
    
    status_color = "green" if invoice['status'] == "Paid" else "red" if invoice['status'] == "Overdue" else "blue"
    st.markdown(f"**Status:** :{status_color}[{invoice['status']}]")
    
    # Header Info
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Customer:** {invoice['customer_name']}")
        st.write(f"**Date:** {invoice['invoice_date'].strftime('%Y-%m-%d')}")
    with col2:
        if invoice['due_date']:
            st.write(f"**Due Date:** {invoice['due_date'].strftime('%Y-%m-%d')}")
        if invoice.get('sales_order_id'):
            st.caption(f"Linked SO ID: {invoice['sales_order_id']}")
            
    st.markdown("---")
    
    # Items
    st.write("**Items:**")
    for item in invoice['items']:
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.write(f"{item['name']}")
        c2.write(f"Qty: {item['quantity']}")
        c3.write(f"₹{item['total']:,.2f}")
    
    st.markdown("---")
    
    # Totals
    c1, c2 = st.columns([3, 1])
    c2.write(f"Subtotal: ₹{invoice['subtotal']:,.2f}")
    c2.write(f"Tax ({invoice['tax_rate']}%): ₹{invoice['tax_amount']:,.2f}")
    c2.markdown(f"**Total: ₹{invoice['total_amount']:,.2f}**")
    
    # Actions
    st.markdown("### Actions")
    if invoice['status'] != 'Paid':
        if st.button("Mark as Paid", key=f"pay_{invoice['_id']}"):
            from models.invoice import Invoice
            Invoice.update_status(invoice['_id'], "Paid")
            st.success("Invoice marked as Paid!")
            st.rerun()

def show():
    """Display the invoices view"""
    if "invoice_success" in st.session_state:
        st.toast(st.session_state.invoice_success, icon="✅")
        del st.session_state.invoice_success
    
    st.title("📝 Invoices")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["All Invoices", "Create Invoice", "Invoice Reports"])
    
    with tab1:
        st.subheader("All Invoices")
        
        from models.invoice import Invoice
        invoices = Invoice.get_all_invoices()
        
        if invoices:
            # Table Header
            c1, c2, c3, c4, c5, c6 = st.columns([1.5, 2, 1.5, 1.5, 1.5, 1])
            c1.markdown("**Invoice #**")
            c2.markdown("**Customer**")
            c3.markdown("**Date**")
            c4.markdown("**Total**")
            c5.markdown("**Status**")
            c6.markdown("**View**")
            
            for inv in invoices:
                c1, c2, c3, c4, c5, c6 = st.columns([1.5, 2, 1.5, 1.5, 1.5, 1])
                c1.write(inv['invoice_number'])
                c2.write(inv['customer_name'])
                c3.write(inv['invoice_date'].strftime('%Y-%m-%d'))
                c4.write(f"₹{inv['total_amount']:,.2f}")
                
                status_color = "green" if inv['status'] == "Paid" else "red" if inv['status'] == "Overdue" else "orange"
                c5.markdown(f":{status_color}[{inv['status']}]")
                
                if c6.button("👁️", key=f"view_inv_{inv['_id']}"):
                    show_invoice_details(inv)
        else:
            st.info("No invoices found.")
            
    with tab2:
        st.subheader("Create New Invoice")
        
        type_choice = st.radio("Create Mode", ["From Sales Order", "Manual Entry"], horizontal=True)
        
        if type_choice == "From Sales Order":
            from models.sales_order import SalesOrder
            orders = SalesOrder.get_all_orders()
            # Filter pending orders basically (or all for now)
            order_opts = {f"{o['order_number']} - {o['customer_name']} (₹{o['total_amount']})": o for o in orders}
            
            
            # Use a key to allow resetting
            selected_so_str = st.selectbox("Select Sales Order", [""] + list(order_opts.keys()), key="so_selector")
            
            if selected_so_str:
                selected_so = order_opts[selected_so_str]
                st.info(f"Generating invoice for {selected_so['customer_name']}")
                
                with st.form("create_invoice_so"):
                    col1, col2 = st.columns(2)
                    with col1:
                        # Use session state to allow clearing, but unique key to avoid conflicts
                        invoice_number = st.text_input("Invoice Number", 
                                                      value=f"INV-{datetime.now().strftime('%Y%m%d')}-{len(orders)}",
                                                      key="so_inv_num")
                        invoice_date = st.date_input("Invoice Date", datetime.now(), key="so_inv_date")
                    with col2:
                        due_date = st.date_input("Due Date", key="so_due_date")
                        st.write(f"**Customer:** {selected_so['customer_name']}")
                        
                    st.write("Items included:")
                    for item in selected_so['items']:
                        st.write(f"- {item['quantity']} x {item['name']} (₹{item['total']})")
                        
                    tax_rate = st.number_input("Tax rate (%)", value=18.0, key="so_tax_rate")
                    notes = st.text_area("Notes", value=f"Based on {selected_so['order_number']}", key="so_notes")
                    
                    def on_invoice_submit():
                        from models.invoice import Invoice
                        inv_id = Invoice.create_invoice(
                            invoice_number=st.session_state.so_inv_num,
                            customer_name=selected_so['customer_name'],
                            invoice_date=st.session_state.so_inv_date,
                            due_date=st.session_state.so_due_date,
                            items=selected_so['items'],
                            tax_rate=st.session_state.so_tax_rate,
                            status="Sent",
                            notes=st.session_state.so_notes,
                            sales_order_id=selected_so['_id'],
                            created_by=st.session_state.user['id'] if st.session_state.user else None
                        )
                        st.session_state.invoice_success = f"Invoice {st.session_state.so_inv_num} generated from Sales Order!"
                        
                        # Clear form fields
                        keys_to_clear = ["so_inv_num", "so_notes", "so_tax_rate", "so_selector"]
                        for key in keys_to_clear:
                            if key in st.session_state: del st.session_state[key]

                    st.form_submit_button("Generate Invoice", type="primary", on_click=on_invoice_submit)

        else:
            # Manual Entry
            if 'inv_items' not in st.session_state: st.session_state.inv_items = []
            
            # Add Item UI (Simplified)
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            with c1: item_name = st.text_input("Item Name", key="manual_item_name")
            with c2: item_qty = st.number_input("Qty", 1, value=1, key="manual_item_qty")
            with c3: item_price = st.number_input("Price", 0.0, value=0.0, key="manual_item_price")
            with c4: 
                st.write("")
                st.write("")
                if st.button("Add"):
                    st.session_state.inv_items.append({
                        "name": item_name, "quantity": item_qty, "price": item_price, "total": item_qty * item_price
                    })
                    st.rerun()
            
            # List items
            for i, item in enumerate(st.session_state.inv_items):
                st.write(f"{i+1}. {item['name']} - {item['quantity']} x {item['price']} = {item['total']}")
                
            with st.form("create_invoice_manual"):
                col1, col2 = st.columns(2)
                with col1:
                    invoice_number = st.text_input("Invoice Number", value=f"INV-{datetime.now().strftime('%Y%m%d')}", key="manual_inv_num")
                    customer_name = st.text_input("Customer Name", key="manual_cust_name")
                with col2:
                    invoice_date = st.date_input("Invoice Date", datetime.now(), key="manual_inv_date")
                    due_date = st.date_input("Due Date", key="manual_due_date")
                    
                tax_rate = st.number_input("Tax Rate (%)", 0.0, key="manual_tax_rate")
                notes = st.text_area("Notes", key="manual_notes")
                
                def on_manual_submit():
                    if not st.session_state.inv_items:
                        st.error("Add items first")
                        return

                    from models.invoice import Invoice
                    Invoice.create_invoice(
                        invoice_number=st.session_state.manual_inv_num,
                        customer_name=st.session_state.manual_cust_name,
                        invoice_date=st.session_state.manual_inv_date,
                        due_date=st.session_state.manual_due_date,
                        items=st.session_state.inv_items,
                        tax_rate=st.session_state.manual_tax_rate,
                        status="Sent",
                        notes=st.session_state.manual_notes,
                        created_by=st.session_state.user['id'] if st.session_state.user else None
                    )
                    st.session_state.inv_items = []

                    st.session_state.invoice_success = f"Invoice {st.session_state.manual_inv_num} created successfully!"
                    
                    # Clear form fields by removing them from session state
                    keys_to_clear = ["manual_inv_num", "manual_cust_name", "manual_notes", "manual_tax_rate"]
                    for key in keys_to_clear:
                        if key in st.session_state:
                            del st.session_state[key]
                            
                st.form_submit_button("Create Invoice", type="primary", on_click=on_manual_submit)

    with tab3:
        st.subheader("Invoice Reports")
        st.info("📊 Invoice analytics and reports coming soon...")
