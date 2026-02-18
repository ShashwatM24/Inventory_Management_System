
import streamlit as st
from models.product import Product
from models.bill import Bill
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show():
    """Display the analytics and reports view"""
    st.title("📈 Analytics & Reports")
    
    # Date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Convert to datetime
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    st.markdown("---")
    
    # Get data
    products = Product.get_all_products()
    bills = Bill.get_bills_by_date_range(start_datetime, end_datetime)
    
    # Calculate metrics
    total_sales = sum(bill['total'] for bill in bills)
    total_bills_count = len(bills)
    avg_bill_value = total_sales / total_bills_count if total_bills_count > 0 else 0
    total_items_sold = sum(sum(item['quantity'] for item in bill['items']) for bill in bills)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sales", f"₹{total_sales:,.2f}")
    
    with col2:
        st.metric("Total Bills", total_bills_count)
    
    with col3:
        st.metric("Avg Bill Value", f"₹{avg_bill_value:,.2f}")
    
    with col4:
        st.metric("Items Sold", total_items_sold)
    
    st.markdown("---")
    
    # Two column layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales trend
        st.subheader("📊 Sales Trend")
        
        if bills:
            # Group by date
            daily_sales = {}
            for bill in bills:
                date_key = bill['created_at'].strftime('%Y-%m-%d')
                daily_sales[date_key] = daily_sales.get(date_key, 0) + bill['total']
            
            sales_df = pd.DataFrame([
                {'Date': date, 'Sales': amount}
                for date, amount in sorted(daily_sales.items())
            ])
            
            fig = px.line(sales_df, x='Date', y='Sales', 
                         title='Daily Sales',
                         markers=True)
            fig.update_layout(yaxis_title="Sales (₹)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data for selected period")
    
    with col2:
        # Top selling products
        st.subheader("🏆 Top Selling Products")
        
        if bills:
            product_sales = {}
            for bill in bills:
                for item in bill['items']:
                    product_name = item['name']
                    product_sales[product_name] = product_sales.get(product_name, 0) + item['quantity']
            
            # Sort and get top 10
            top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:10]
            
            if top_products:
                top_df = pd.DataFrame(top_products, columns=['Product', 'Quantity Sold'])
                
                fig = px.bar(top_df, x='Quantity Sold', y='Product', 
                            orientation='h',
                            title='Top 10 Products by Quantity')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data for selected period")
    
    st.markdown("---")
    
    # Revenue by category
    st.subheader("💰 Revenue by Category")
    
    if bills and products:
        category_revenue = {}
        
        for bill in bills:
            for item in bill['items']:
                # Find product to get category
                product = next((p for p in products if p['name'] == item['name']), None)
                if product:
                    category = product.get('category', 'Uncategorized')
                    category_revenue[category] = category_revenue.get(category, 0) + item['total']
        
        if category_revenue:
            cat_df = pd.DataFrame([
                {'Category': cat, 'Revenue': rev}
                for cat, rev in category_revenue.items()
            ])
            
            fig = px.pie(cat_df, values='Revenue', names='Category',
                        title='Revenue Distribution by Category')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No revenue data available")
    
    st.markdown("---")
    
    # Inventory valuation
    st.subheader("📦 Inventory Valuation")
    
    if products:
        col1, col2 = st.columns(2)
        
        with col1:
            # Total inventory value
            total_value = sum(p.get('stock', 0) * p['price'] for p in products)
            total_cost = sum(p.get('stock', 0) * p['cost'] for p in products)
            potential_profit = total_value - total_cost
            
            st.metric("Total Inventory Value", f"₹{total_value:,.2f}")
            st.metric("Total Cost", f"₹{total_cost:,.2f}")
            st.metric("Potential Profit", f"₹{potential_profit:,.2f}")
        
        with col2:
            # Category-wise valuation
            category_value = {}
            for p in products:
                cat = p.get('category', 'Uncategorized')
                category_value[cat] = category_value.get(cat, 0) + (p.get('stock', 0) * p['price'])
            
            val_df = pd.DataFrame([
                {'Category': cat, 'Value': val}
                for cat, val in category_value.items()
            ])
            
            fig = px.bar(val_df, x='Category', y='Value',
                        title='Inventory Value by Category')
            fig.update_layout(yaxis_title="Value (₹)")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No inventory data available")
    
    st.markdown("---")
    
    # Stock movement
    st.subheader("📊 Stock Movement Analysis")
    
    stock_movements = Product.get_stock_movements(limit=100)
    
    if stock_movements:
        movements_data = []
        for movement in stock_movements:
            product = Product.get_product_by_id(str(movement['product_id']))
            if product:
                movements_data.append({
                    'Date': movement['timestamp'].strftime('%Y-%m-%d %H:%M'),
                    'Product': product['name'],
                    'Type': movement['movement_type'],
                    'Change': movement['quantity_change'],
                    'Notes': movement.get('notes', '')
                })
        
        if movements_data:
            movements_df = pd.DataFrame(movements_data)
            st.dataframe(movements_df, use_container_width=True, hide_index=True)
    else:
        st.info("No stock movement data available")
    
    # Export functionality
    st.markdown("---")
    st.subheader("📥 Export Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if bills:
            bills_export = pd.DataFrame([{
                'Bill Number': b['bill_number'],
                'Customer': b['customer_name'],
                'Contact': b['customer_contact'],
                'Total': b['total'],
                'Date': b['created_at'].strftime('%Y-%m-%d %H:%M')
            } for b in bills])
            
            csv = bills_export.to_csv(index=False)
            st.download_button(
                label="📄 Export Bills (CSV)",
                data=csv,
                file_name=f"bills_{start_date}_to_{end_date}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col2:
        if products:
            products_export = pd.DataFrame([{
                'SKU': p['sku'],
                'Name': p['name'],
                'Category': p['category'],
                'Quantity': p.get('stock', 0),
                'Price': p['price'],
                'Value': p.get('stock', 0) * p['price']
            } for p in products])
            
            csv = products_export.to_csv(index=False)
            st.download_button(
                label="📦 Export Inventory (CSV)",
                data=csv,
                file_name=f"inventory_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col3:
        if stock_movements and movements_data:
            movements_export = pd.DataFrame(movements_data)
            csv = movements_export.to_csv(index=False)
            st.download_button(
                label="📊 Export Movements (CSV)",
                data=csv,
                file_name=f"stock_movements_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
