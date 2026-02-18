
import streamlit as st
from services.ai_service import chat_with_ai, stream_ai_response, get_full_business_context, compress_with_scaledown
from models.purchase_order import PurchaseOrder
from models.supplier import Supplier

from datetime import datetime
import json
import plotly.express as px

import pandas as pd
import re
from PIL import Image
from urllib.parse import quote

def extract_json_from_response(text):
    """Extract JSON block from text"""
    try:
        # Find JSON between ```json and ```
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        return None
    except:
        return None

def render_action_ui(json_data, key_suffix):
    """Render UI elements for actions (in history or new)"""
    try:
        action = json_data.get("action")
        data = json_data.get("data", {})
        
        if action == "draft_email":
            recipient = data.get("recipient", "[No Recipient]")
            subject = data.get("subject", "[No Subject]")
            body = data.get("body", "")
            
            with st.expander("📧 Email Draft", expanded=True):
                st.markdown(f"**To:** `{recipient}`")
                st.markdown(f"**Subject:** `{subject}`")
                st.text_area("Content", value=body, height=200, disabled=False, label_visibility="collapsed", key=f"email_content_{key_suffix}")
                
                # Create mailto link
                subject_enc = quote(subject)
                body_enc = quote(body)
                mailto_link = f"mailto:{recipient}?subject={subject_enc}&body={body_enc}"
                
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.info("Copy the content above.")
                with c2:
                    st.link_button("🚀 Send via Email App", mailto_link, use_container_width=True)
                
        elif action == "create_po":
            # PO creation already has toast/balloons when executed. 
            # In history, we just show a static confirmation.
            st.success(f"✅ Purchase Order Created for **{data.get('supplier_name')}**")
            
    except Exception as e:
        st.error(f"Error rendering action UI: {e}")

def execute_action(json_data):
    """Execute an action from AI"""
    try:
        action = json_data.get("action")
        data = json_data.get("data")
        
        if action == "create_po":
            supplier_name = data.get("supplier_name", "Unknown")
            items = data.get("items", [])
            
            if not items:
                st.error("Action Failed: No items to order.")
                return

            # Check for unknown supplier
            if supplier_name.upper() in ["UNKNOWN", "UNKNOWN_SUPPLIER", "PLEASE SPECIFY SUPPLIER"]:
                st.session_state.pending_po = data
                st.session_state.show_supplier_selector = True
                st.rerun()
                return

            # Use helper for PO creation
            create_po_logic(data, supplier_name)
            
        elif action == "draft_email":
            # No side effect for drafting email, just UI rendering
            pass
                
    except Exception as e:
        st.error(f"Action Execution Error: {e}")

def render_chart(json_data):
    """Render chart based on JSON data"""
    try:
        chart_type = json_data.get("type")
        data = json_data.get("data")
        title = json_data.get("title", "Chart")
        
        if not data:
            return
            
        df = pd.DataFrame(list(data.items()), columns=["Label", "Value"])
        
        if chart_type == "pie":
            fig = px.pie(df, values='Value', names='Label', title=title)
        elif chart_type == "bar":
            fig = px.bar(df, x='Label', y='Value', title=title)
        elif chart_type == "line":
            fig = px.line(df, x='Label', y='Value', title=title)
        else:
            return

        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering chart: {e}")

def create_po_logic(data, supplier_name):
    """Helper to create PO from AI data"""
    items = data.get("items", [])
    if not items:
        st.error("Action Failed: No items to order.")
        return False
        
    po_items = []
    for item in items:
        qty = float(item.get("quantity", 0))
        price = float(item.get("price", 0))
        po_items.append({
            "product_id": item.get("product_id"),
            "name": item.get("name"),
            "quantity": qty,
            "price": price,
            "total": qty * price
        })
    
    po_number = f"PO-AI-{datetime.now().strftime('%Y%m%d%H%M')}"
    
    po_id = PurchaseOrder.create_po(
        po_number=po_number,
        supplier_id=None, # In a real app, we'd look this up
        supplier_name=supplier_name,
        order_date=datetime.now(),
        expected_delivery=None,
        items=po_items,
        status="Draft",
        notes="Generated by AI Assistant"
    )
    
    if po_id:
        st.toast(f"✅ Created Draft PO: {po_number}")
        st.balloons()
        st.success(f"Action Complete: Created Purchase Order **{po_number}** for **{supplier_name}**.")
        return True
    return False

def handle_supplier_selection():
    """Handle the UI for selecting a supplier if missing"""
    if st.session_state.get('show_supplier_selector'):
        with st.container():
            st.warning("⚠️ **Supplier Missing**: The AI needs you to select a supplier for this order.")
            
            suppliers = Supplier.get_all_suppliers()
            supplier_names = [s.get('name') for s in suppliers]
            if not supplier_names:
                supplier_names = ["Generic Supplier", "Local Vendor"]
            
            selected_supplier = st.selectbox("Select Supplier", supplier_names, key="sup_select")
            
            c1, c2 = st.columns(2)
            if c1.button("Confirm Order", type="primary"):
                data = st.session_state.get('pending_po')
                if create_po_logic(data, selected_supplier):
                    # Add to history
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": f"Action Complete: Created Purchase Order for **{selected_supplier}**."
                    })
                    # Clear state
                    st.session_state.show_supplier_selector = False
                    st.session_state.pending_po = None
                    st.rerun()
            
            if c2.button("Cancel Order"):
                st.session_state.show_supplier_selector = False
                st.session_state.pending_po = None
                st.rerun()
            st.divider()

def show():
    """Display the AI chat view"""
    st.title("🤖 AI Inventory Assistant")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    
    # Display chat history
    for i, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            # Hide JSON from display
            clean_content = re.sub(r"```(json)?\s*(.*?)\s*```", "", message["content"], flags=re.DOTALL).strip()
            if clean_content:
                st.markdown(clean_content)
            
            # Check for chart or logic in history
            if message["role"] == "assistant":
                json_data = extract_json_from_response(message["content"])
                if json_data:
                    if json_data.get("type") == "action":
                         render_action_ui(json_data, key_suffix=f"hist_{i}")
                    else:
                        render_chart(json_data)
    
    # Handle pending supplier selection (moved to bottom)
    handle_supplier_selection()
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your inventory..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Display assistant response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream response
            with st.spinner("Thinking..."):
                try:
                    response_stream = stream_ai_response(prompt, image_data=image_data)
                    # Force first chunk to trigger spinner wait
                    first_chunk = next(response_stream, "")
                except Exception as e:
                    first_chunk = f"⚠️ Error: {str(e)}"
                    response_stream = []

            full_response += first_chunk
            message_placeholder.markdown(full_response + "▌")
            
            for chunk in response_stream:
                full_response += chunk
                # Provide a clean preview during streaming (optional, or just stream dots)
                # For now, we will stream the raw text but clean it up immediately after
                message_placeholder.markdown(full_response + "▌")
            
            # Clean up JSON from final display
            clean_response = re.sub(r"```(json)?\s*(.*?)\s*```", "", full_response, flags=re.DOTALL).strip()
            if not clean_response:
                # If response was ONLY JSON, show a friendly status
                clean_response = "✅ Action processed."
            
            message_placeholder.markdown(clean_response)
            
            # Check for JSON in new response
            json_data = extract_json_from_response(full_response)
            if json_data:
                if json_data.get("type") == "action":
                    execute_action(json_data)
                    render_action_ui(json_data, key_suffix="new")
                else:
                    render_chart(json_data)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})
    
    # Welcome message if no chat history
    if not st.session_state.chat_history:
        st.info("""
        👋 **Welcome to the AI Inventory Assistant!**
        
        I can help you with:
        - 📦 Product information and availability
        - ⚠️ Low stock alerts and recommendations
        - 📊 Sales and inventory analytics
        - 🔍 Finding specific products
        - 💡 Inventory management suggestions
        
        Try asking me a question or use the sample questions in the sidebar!
        """)
