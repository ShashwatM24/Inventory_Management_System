
import streamlit as st
from datetime import datetime


@st.dialog("Order Details")
def show_order_details(order):
    """Display order details in a dialog"""
    st.subheader(f"Order: {order['order_number']}")
    
    # Customer Info
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Customer:** {order['customer_name']}")
    with col2:
        st.write(f"**Date:** {order['order_date'].strftime('%Y-%m-%d')}")
    
    st.markdown("---")
    
    # Items
    st.write("**Items:**")
    for item in order['items']:
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.write(f"{item['name']}")
        c2.write(f"Qty: {item['quantity']}")
        c3.write(f"₹{item['total']:,.2f}")
    
    st.markdown("---")
    
    # Footer
    col1, col2 = st.columns(2)
    with col1:
        if order.get('notes'):
            st.info(f"📝 {order['notes']}")
    with col2:
        st.metric("Total Amount", f"₹{order['total_amount']:,.2f}")


def show():
    """Display the sales orders view"""
    st.title("🛒 Sales Orders")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["All Orders", "Create Order", "Order History"])
    
    with tab1:
# ... (rest of tab1 implementation remains same, skipping for brevity in replacement) ...
        st.subheader("All Sales Orders")
        st.info("📋 Sales orders management coming soon...")
        
        # Placeholder for sales orders list
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Orders", "0", "0")
        with col2:
            st.metric("Pending", "0", "0")
        with col3:
            st.metric("Completed", "0", "0")
    
    with tab2:
# ... (tab2 implementation) ...
        st.subheader("Create New Sales Order")
        
        if 'sales_order_items' not in st.session_state:
            st.session_state.sales_order_items = []

        # Customer Details
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                customer_name = st.text_input("Customer Name")
                order_date = st.date_input("Order Date", datetime.now())
            with col2:
                order_number = st.text_input("Order Number", f"SO-{datetime.now().strftime('%Y%m%d')}")
                delivery_date = st.date_input("Expected Delivery")

        st.markdown("---")

        # Product Selection
        st.subheader("Add Items")
        
        # Get products
        from models.product import Product
        products = Product.get_all_products()
        product_options = [""] + [f"{p['name']} - {p['sku']} (Stock: {p.get('stock', 0)})" for p in products]

        if products:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                selected_product_str = st.selectbox("Select Product", product_options, key="so_product_select")
            with col2:
                quantity = st.number_input("Quantity", min_value=1, value=1, key="so_quantity")
            with col3:
                st.write("")
                st.write("")
                if st.button("➕ Add Item", use_container_width=True):
                    if not selected_product_str:
                        st.error("⚠️ Please select a product")
                    else:
                        try:
                            # Subtract 1 because of the added empty option
                            selected_index = product_options.index(selected_product_str) - 1
                            if selected_index >= 0:
                                product = products[selected_index]
                                
                                # Add to items list
                                item = {
                                    'product_id': str(product['_id']),
                                    'name': product['name'],
                                    'sku': product['sku'],
                                    'quantity': quantity,
                                    'price': product.get('price', 0.0),
                                    'total': quantity * product.get('price', 0.0)
                                }
                                st.session_state.sales_order_items.append(item)
                                st.success(f"Added {quantity} x {product['name']}")
                                st.rerun()
                            else:
                                st.error("❌ Invalid product selection")
                        except Exception as e:
                            st.error(f"Error adding item: {e}")
        else:
            st.warning("No products available")

        # Display Items
        if st.session_state.sales_order_items:
            st.markdown("### Order Items")
            
            # Header
            c1, c2, c3, c4, c5 = st.columns([3, 1, 1.5, 1.5, 0.5])
            c1.markdown("**Product**")
            c2.markdown("**Qty**")
            c3.markdown("**Price**")
            c4.markdown("**Total**")
            c5.markdown("")

            # Items
            for i, item in enumerate(st.session_state.sales_order_items):
                c1, c2, c3, c4, c5 = st.columns([3, 1, 1.5, 1.5, 0.5])
                c1.write(f"{item['name']} ({item['sku']})")
                c2.write(str(item['quantity']))
                c3.write(f"₹{item['price']:,.2f}")
                c4.write(f"₹{item['total']:,.2f}")
                
                if c5.button("❌", key=f"so_remove_{i}"):
                    st.session_state.sales_order_items.pop(i)
                    st.rerun()

            # Totals
            total_amount = sum(item['total'] for item in st.session_state.sales_order_items)
            st.markdown(f"### **Total Amount: ₹{total_amount:,.2f}**")

        st.markdown("---")
        notes = st.text_area("Notes")

        if st.button("Create Sales Order", type="primary", use_container_width=True):
            if not customer_name:
                st.error("Please enter customer name")
            elif not st.session_state.sales_order_items:
                st.error("Please add items to the order")
            else:
                try:
                    from models.sales_order import SalesOrder
                    
                    # Create order in DB
                    order_id = SalesOrder.create_order(
                        order_number=order_number,
                        customer_name=customer_name,
                        order_date=order_date,
                        delivery_date=delivery_date,
                        items=st.session_state.sales_order_items,
                        notes=notes,
                        created_by=st.session_state.user['id'] if st.session_state.user else None
                    )
                    
                    if order_id:
                        st.toast("✅ Sales Order Placed Successfully!", icon="🎉")
                        st.success(f"Order {order_number} created!")
                        
                        # Clear form
                        st.session_state.sales_order_items = []
                        st.rerun()
                    else:
                        st.error("Failed to create order")
                except Exception as e:
                    st.error(f"Error creating order: {e}")
    
    with tab3:
        st.subheader("Order History")
        
        from models.sales_order import SalesOrder
        orders = SalesOrder.get_all_orders()
        
        if orders:
            # Table Header
            c1, c2, c3, c4, c5, c6 = st.columns([1.5, 2, 1.5, 1.5, 1.5, 1])
            c1.markdown("**Order #**")
            c2.markdown("**Customer**")
            c3.markdown("**Date**")
            c4.markdown("**Total**")
            c5.markdown("**Status**")
            c6.markdown("**View**")
            
            for order in orders:
                c1, c2, c3, c4, c5, c6 = st.columns([1.5, 2, 1.5, 1.5, 1.5, 1])
                c1.write(order['order_number'])
                c2.write(order['customer_name'])
                c3.write(order['order_date'].strftime('%Y-%m-%d'))
                c4.write(f"₹{order['total_amount']:,.2f}")
                
                status_color = "orange" if order['status'] == "Pending" else "green"
                status_icon = "⏳" if order['status'] == "Pending" else "✅"
                c5.markdown(f":{status_color}[{status_icon} {order['status']}]")
                
                if c6.button("👁️", key=f"view_{order['_id']}", help="View Order Details"):
                    show_order_details(order)
                    
        else:
            st.info("No sales orders found.")
