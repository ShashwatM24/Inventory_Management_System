
import streamlit as st
from datetime import datetime

def show():
    """Display the purchase orders view"""
    st.title("🛍️ Purchase Orders")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["All Orders", "Create Order", "Order History"])
    
@st.dialog("Purchase Order Details")
def show_po_details(po):
    """Display PO details in a dialog"""
    st.subheader(f"PO: {po['po_number']}")
    
    status_color = "green" if po['status'] == "Received" else "blue" if po['status'] == "Sent" else "orange"
    st.markdown(f"**Status:** :{status_color}[{po['status']}]")
    
    # Header Info
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Supplier:** {po['supplier_name']}")
        st.write(f"**Order Date:** {po['order_date'].strftime('%Y-%m-%d')}")
    with col2:
        if po.get('expected_delivery'):
            st.write(f"**Expected Delivery:** {po['expected_delivery'].strftime('%Y-%m-%d')}")
            
    st.markdown("---")
    
    # Items
    st.write("**Items:**")
    for item in po['items']:
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.write(f"{item['name']}")
        c2.write(f"Qty: {item['quantity']}")
        c3.write(f"₹{item['total']:,.2f}")
    
    st.markdown("---")
    st.markdown(f"### Total: ₹{po['total_amount']:,.2f}")
    
    # Actions
    st.markdown("### Actions")
    if po['status'] != 'Received':
        if st.button("Mark as Received", key=f"r_{po['_id']}"):
            from models.purchase_order import PurchaseOrder
            PurchaseOrder.update_status(po['_id'], "Received")
            # TODO: Add logic to update stock levels here
            st.success("Order marked as Received!")
            st.rerun()

def show():
    """Display the purchase orders view"""
    if "po_success" in st.session_state:
        st.toast(st.session_state.po_success, icon="✅")
        del st.session_state.po_success

    st.title("🛍️ Purchase Orders")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["All Orders", "Create Order", "Order History"])
    
    with tab1:
        st.subheader("All Purchase Orders")
        
        from models.purchase_order import PurchaseOrder
        pos = PurchaseOrder.get_all_pos()
        
        if pos:
            # Table Header
            c1, c2, c3, c4, c5, c6 = st.columns([1.5, 2, 1.5, 1.5, 1.5, 1])
            c1.markdown("**PO #**")
            c2.markdown("**Supplier**")
            c3.markdown("**Date**")
            c4.markdown("**Total**")
            c5.markdown("**Status**")
            c6.markdown("**View**")
            
            for po in pos:
                c1, c2, c3, c4, c5, c6 = st.columns([1.5, 2, 1.5, 1.5, 1.5, 1])
                c1.write(po['po_number'])
                c2.write(po['supplier_name'])
                c3.write(po['order_date'].strftime('%Y-%m-%d'))
                c4.write(f"₹{po['total_amount']:,.2f}")
                
                status_color = "green" if po['status'] == "Received" else "blue" if po['status'] == "Sent" else "orange"
                c5.markdown(f":{status_color}[{po['status']}]")
                
                if c6.button("👁️", key=f"view_po_{po['_id']}"):
                    show_po_details(po)
        else:
            st.info("No purchase orders found.")
            
    with tab2:
        st.subheader("Create Purchase Order")
        
        # Initialize item list
        if 'po_items' not in st.session_state: st.session_state.po_items = []
        
        # 1. Select Supplier
        from models.supplier import Supplier
        suppliers = Supplier.get_all_suppliers()
        supp_opts = {s['name']: s for s in suppliers}
        if not supp_opts:
            st.warning("No suppliers found. Please add suppliers first.")
        else:
            selected_supp_name = st.selectbox("Select Supplier", list(supp_opts.keys()), key="po_supp_select")
            
            # 2. Add Items
            st.markdown("#### Add Items")
            from models.product import Product
            products = Product.get_all_products()
            prod_opts = {p['name']: p for p in products}
            
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            with c1: 
                sel_prod_name = st.selectbox("Product", [""] + list(prod_opts.keys()), key="po_prod_select")
            with c2: 
                qty = st.number_input("Qty", 1, value=1, key="po_qty")
            
            # Auto-fill cost if product selected
            cost_val = 0.0
            if sel_prod_name and sel_prod_name in prod_opts:
                cost_val = prod_opts[sel_prod_name].get('cost', 0.0)
                
            with c3: 
                cost = st.number_input("Unit Cost", 0.0, value=float(cost_val), key="po_cost")
                
            with c4: 
                st.write("")
                st.write("")
                if st.button("Add Item", key="po_add_btn"):
                    if sel_prod_name:
                        st.session_state.po_items.append({
                            "name": sel_prod_name,
                            "product_id": prod_opts[sel_prod_name]['_id'],
                            "quantity": qty,
                            "unit_price": cost,
                            "total": qty * cost
                        })
                        st.rerun()
            
            # List Items
            if st.session_state.po_items:
                st.markdown("##### Selected Items")
                for i, item in enumerate(st.session_state.po_items):
                    st.write(f"{i+1}. {item['name']} - {item['quantity']} x ₹{item['unit_price']} = ₹{item['total']}")
                st.divider()

            # 3. Create PO Form
            with st.form("create_po_form"):
                c1, c2 = st.columns(2)
                with c1:
                    po_number = st.text_input("PO Number", value=f"PO-{datetime.now().strftime('%Y%m%d')}-{len(pos)+1}", key="po_num")
                    order_date = st.date_input("Order Date", datetime.now(), key="po_date")
                    
                with c2:
                    expected_delivery = st.date_input("Expected Delivery", key="po_delivery")
                    status = st.selectbox("Status", ["Draft", "Sent", "Confirmed"], key="po_status")
                    
                notes = st.text_area("Notes", key="po_notes")
                
                # Callback for submission
                def on_create_po():
                    if not st.session_state.po_items:
                        st.error("Please add at least one item.")
                        return
                    
                    from models.purchase_order import PurchaseOrder
                    PurchaseOrder.create_po(
                        po_number=st.session_state.po_num,
                        supplier_id=supp_opts[st.session_state.po_supp_select]['_id'],
                        supplier_name=st.session_state.po_supp_select,
                        order_date=st.session_state.po_date,
                        expected_delivery=st.session_state.po_delivery,
                        items=st.session_state.po_items,
                        status=st.session_state.po_status,
                        notes=st.session_state.po_notes,
                        created_by=st.session_state.user['id'] if st.session_state.user else None
                    )
                    
                    st.session_state.po_success = f"Purchase Order {st.session_state.po_num} Created!"
                    
                    # Clear state
                    st.session_state.po_items = []
                    keys_to_clear = ["po_num", "po_notes", "po_supp_select", "po_prod_select", "po_cost", "po_qty"]
                    for k in keys_to_clear:
                        if k in st.session_state: del st.session_state[k]
                        
                st.form_submit_button("Create Purchase Order", type="primary", on_click=on_create_po)

    with tab3:
        st.subheader("📊 Purchase Order Analytics")
        
        from models.purchase_order import PurchaseOrder
        import pandas as pd
        
        # 1. Fetch Data
        all_pos = PurchaseOrder.get_all_pos(limit=1000) # Fetch more for history
        
        if not all_pos:
            st.info("No purchase order data available for analysis.")
        else:
            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(all_pos)
            
            # Ensure dates are datetime objects
            df['order_date'] = pd.to_datetime(df['order_date'])
            
            # --- Sidebar / Top Bar Filters ---
            with st.expander("🔎 Filter Options", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Date Range Filter
                    min_date = df['order_date'].min().date()
                    max_date = df['order_date'].max().date()
                    start_date = st.date_input("Start Date", min_date)
                    end_date = st.date_input("End Date", max_date)
                
                with col2:
                    # Supplier Filter
                    unique_suppliers = sorted(df['supplier_name'].unique().tolist())
                    selected_suppliers = st.multiselect("Select Suppliers", unique_suppliers)
                    
                with col3:
                    # Status Filter
                    unique_statuses = sorted(df['status'].unique().tolist())
                    selected_statuses = st.multiselect("Select Status", unique_statuses)
            
            # --- Apply Filters ---
            mask = (df['order_date'].dt.date >= start_date) & (df['order_date'].dt.date <= end_date)
            
            if selected_suppliers:
                mask &= (df['supplier_name'].isin(selected_suppliers))
            
            if selected_statuses:
                mask &= (df['status'].isin(selected_statuses))
            
            filtered_df = df.loc[mask]
            
            if filtered_df.empty:
                st.warning("No orders match the selected filters.")
            else:
                # --- Analytics Metrics ---
                st.markdown("### 📈 Key Metrics")
                m1, m2, m3, m4 = st.columns(4)
                
                total_spend = filtered_df['total_amount'].sum()
                po_count = len(filtered_df)
                avg_value = total_spend / po_count if po_count > 0 else 0
                received_count = len(filtered_df[filtered_df['status'] == 'Received'])
                
                m1.metric("Total Spend", f"₹{total_spend:,.2f}")
                m2.metric("Orders Processed", str(po_count))
                m3.metric("Avg. Order Value", f"₹{avg_value:,.2f}")
                m4.metric("Completed Orders", str(received_count))
                
                st.markdown("---")
                
                # --- Detailed Data Table ---
                st.subheader(f"Detailed History ({len(filtered_df)} Orders)")
                
                # Format for display
                display_df = filtered_df[['po_number', 'supplier_name', 'order_date', 'total_amount', 'status', 'expected_delivery']].copy()
                display_df.columns = ['PO #', 'Supplier', 'Date', 'Total Amount', 'Status', 'Expected Delivery']
                # Format dates
                display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
                
                st.dataframe(
                    display_df,
                    column_config={
                        "Total Amount": st.column_config.NumberColumn(format="₹%.2f"),
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                # --- Export ---
                col_left, col_right = st.columns([4, 1])
                with col_right:
                    csv = display_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv,
                        file_name=f"po_history_{start_date}_{end_date}.csv",
                        mime="text/csv",
                    )
