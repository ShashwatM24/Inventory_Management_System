
import streamlit as st
from models.product import Product
from models.supplier import Supplier
import pandas as pd

def show():
    """Display the inventory management view"""
    st.title("📦 Inventory Management")
    
    # Tabs for different operations
    tab1, tab2, tab3 = st.tabs(["📋 View Products", "➕ Add Product", "🔍 Search & Filter"])
    
    # Tab 1: View Products
    with tab1:
        st.subheader("All Products")
        
        products = Product.get_all_products()
        
        if products:
            # Convert to dataframe
            products_data = []
            for p in products:
                products_data.append({
                    'SKU': p.get('sku', 'Unknown'),
                    'Name': p.get('name', 'Unknown'),
                    'Category': p.get('category', 'Uncategorized'),
                    'Quantity': p.get('stock', 0),
                    'Unit': p.get('unit', 'pcs'),
                    'Price': f"₹{p.get('price', 0.0):,.2f}",
                    'Cost': f"₹{p.get('cost', 0.0):,.2f}",
                    'Reorder Level': p.get('reorder_level', 10),
                    'Status': '⚠️ Low Stock' if p.get('stock', 0) <= p.get('reorder_level', 10) else '✅ In Stock'
                })
            
            df = pd.DataFrame(products_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Product management
            st.markdown("---")
            st.subheader("🛠️ Manage Products")
            
            # Select product to edit/delete
            product_names = [f"{p['name']} ({p['sku']})" for p in products]
            selected_product = st.selectbox("Select Product", product_names)
            
            if selected_product:
                # Find the selected product
                selected_sku = selected_product.split('(')[1].strip(')')
                product = Product.get_product_by_sku(selected_sku)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Edit product
                    with st.expander("✏️ Edit Product"):
                        with st.form("edit_product_form"):
                            new_name = st.text_input("Name", value=product.get('name', ''))
                            new_desc = st.text_area("Description", value=product.get('description', ''))
                            new_category = st.text_input("Category", value=product.get('category', 'Uncategorized'))
                            new_quantity = st.number_input("Quantity", value=product.get('stock', 0), min_value=0)
                            new_unit = st.text_input("Unit", value=product.get('unit', 'pcs'))
                            new_price = st.number_input("Price", value=float(product.get('price', 0.0)), min_value=0.0, step=0.01)
                            new_cost = st.number_input("Cost", value=float(product.get('cost', 0.0)), min_value=0.0, step=0.01)
                            new_reorder = st.number_input("Reorder Level", value=product.get('reorder_level', 10), min_value=0)
                            
                            if st.form_submit_button("💾 Save Changes", use_container_width=True):
                                updates = {
                                    'name': new_name,
                                    'description': new_desc,
                                    'category': new_category,
                                    'stock': new_quantity,
                                    'unit': new_unit,
                                    'price': new_price,
                                    'cost': new_cost,
                                    'reorder_level': new_reorder
                                }
                                Product.update_product(str(product['_id']), updates)
                                st.success("✅ Product updated successfully!")
                                st.rerun()
                
                with col2:
                    # Stock adjustment
                    with st.expander("📊 Adjust Stock"):
                        with st.form("adjust_stock_form"):
                            adjustment = st.number_input("Quantity Change", value=0, 
                                                        help="Positive to add, negative to reduce")
                            movement_type = st.selectbox("Movement Type", 
                                                        ["adjustment", "purchase", "return", "damage"])
                            notes = st.text_area("Notes")
                            
                            if st.form_submit_button("🔄 Adjust Stock", use_container_width=True):
                                if adjustment != 0:
                                    success = Product.update_stock(
                                        str(product['_id']), 
                                        adjustment, 
                                        movement_type, 
                                        notes
                                    )
                                    if success:
                                        st.success(f"✅ Stock adjusted by {adjustment}")
                                        st.rerun()
                                    else:
                                        st.error("❌ Cannot reduce stock below 0")
                                else:
                                    st.warning("⚠️ Please enter a non-zero adjustment")
                    
                    # Delete product
                    with st.expander("🗑️ Delete Product"):
                        st.warning("⚠️ This action cannot be undone!")
                        if st.button("🗑️ Delete Product", type="primary", use_container_width=True):
                            Product.delete_product(str(product['_id']))
                            st.success("✅ Product deleted successfully!")
                            st.rerun()
        else:
            st.info("📦 No products found. Add your first product!")
    
    # Tab 2: Add Product
    with tab2:
        st.subheader("Add New Product")
        
        # Get suppliers for dropdown
        suppliers = Supplier.get_all_suppliers()
        supplier_options = ["None"] + [f"{s['name']} ({s['_id']})" for s in suppliers]
        
        with st.form("add_product_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Product Name *", placeholder="e.g., Laptop Dell XPS 15")
                description = st.text_area("Description", placeholder="Product details...")
                category = st.text_input("Category *", placeholder="e.g., Electronics")
                quantity = st.number_input("Initial Quantity *", min_value=0, value=0)
                unit = st.text_input("Unit *", value="pcs", placeholder="e.g., pcs, kg, ltr")
            
            with col2:
                price = st.number_input("Selling Price (₹) *", min_value=0.0, value=0.0, step=0.01)
                cost = st.number_input("Cost Price (₹) *", min_value=0.0, value=0.0, step=0.01)
                reorder_level = st.number_input("Reorder Level *", min_value=0, value=10,
                                               help="Minimum stock level for alerts")
                supplier = st.selectbox("Supplier", supplier_options)
            
            submitted = st.form_submit_button("➕ Add Product", use_container_width=True)
            
            if submitted:
                if not all([name, category, unit]):
                    st.error("❌ Please fill all required fields marked with *")
                elif price <= 0 or cost <= 0:
                    st.error("❌ Price and cost must be greater than 0")
                else:
                    # Extract supplier ID if selected
                    supplier_id = None
                    if supplier != "None":
                        supplier_id = supplier.split('(')[1].strip(')')
                    
                    product_id = Product.create_product(
                        name=name,
                        description=description,
                        category=category,
                        stock=quantity,
                        unit=unit,
                        price=price,
                        cost=cost,
                        reorder_level=reorder_level,
                        supplier_id=supplier_id
                    )
                    
                    if product_id:
                        st.success(f"✅ Product added successfully! SKU: {Product.get_product_by_id(product_id)['sku']}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add product")
    
    # Tab 3: Search & Filter
    with tab3:
        st.subheader("Search & Filter Products")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_term = st.text_input("🔍 Search", placeholder="Search by name, SKU, category...")
        
        with col2:
            filter_category = st.selectbox("Filter by Category", 
                                          ["All"] + Product.get_categories())
        
        # Apply filters
        if search_term:
            filtered_products = Product.search_products(search_term)
        else:
            filtered_products = Product.get_all_products()
        
        if filter_category != "All":
            filtered_products = [p for p in filtered_products if p['category'] == filter_category]
        
        # Display results
        if filtered_products:
            st.write(f"Found {len(filtered_products)} product(s)")
            
            products_data = []
            for p in filtered_products:
                products_data.append({
                    'SKU': p.get('sku', 'Unknown'),
                    'Name': p.get('name', 'Unknown'),
                    'Category': p.get('category', 'Uncategorized'),
                    'Quantity': p.get('stock', 0),
                    'Unit': p.get('unit', 'pcs'),
                    'Price': f"₹{p.get('price', 0.0):,.2f}",
                    'Status': '⚠️ Low Stock' if p.get('stock', 0) <= p.get('reorder_level', 10) else '✅ In Stock'
                })
            
            df = pd.DataFrame(products_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No products found matching your criteria")
