"""
AI Chat Page - Gemini-powered Chatbot
"""
import streamlit as st
from services.ai_service import chat_with_ai, stream_ai_response, get_inventory_context, compress_with_scaledown

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

st.title("🤖 AI Inventory Assistant")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar with context info
with st.sidebar:
    st.subheader("📊 Context Information")
    
    # Show compression stats
    if st.button("🔄 Refresh Context"):
        context = get_inventory_context()
        compressed, stats = compress_with_scaledown(context)
        
        if stats:
            st.success("✅ Context compressed with Scaledown API")
            st.metric("Original Tokens", stats['original_tokens'])
            st.metric("Compressed Tokens", stats['compressed_tokens'])
            st.metric("Compression Ratio", f"{stats['compression_ratio']:.2f}x")
        else:
            st.info("ℹ️ Using uncompressed context")
            st.metric("Context Size", f"{len(context.split())} words")
    
    st.markdown("---")
    
    # Sample questions
    st.subheader("💡 Sample Questions")
    sample_questions = [
        "What products are low in stock?",
        "Show me all products in Electronics category",
        "What is the total inventory value?",
        "Which products should I reorder?",
        "Show me recent sales",
        "What are the top selling products?",
        "How many products do we have?",
        "What is the average product price?"
    ]
    
    for question in sample_questions:
        if st.button(question, key=f"sample_{question}", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": question})
            st.rerun()
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

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
        for chunk in stream_ai_response(prompt):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
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
