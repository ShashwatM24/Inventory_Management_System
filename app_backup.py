"""
Main Streamlit Application - Inventory Management System
Entry point with authentication
"""
import streamlit as st
from models.user import User
from config.database import init_db

# Page configuration
st.set_page_config(
    page_title="Vaultly - Inventory Management",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
try:
    init_db()
except Exception as e:
    st.error(f"Failed to connect to database: {e}")
    st.stop()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None


def show_auth_sidebar():
    """Display minimal sidebar for login/register pages"""
    # Hide the navigation menu using CSS
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Center and display logo image
    col1, col2, col3 = st.sidebar.columns([1, 2, 1])
    with col2:
        st.image("static/vaultly_logo.png", use_container_width=True)
    
    st.sidebar.markdown("""
        <div style='text-align: center; padding: 0.5rem 0;'>
            <h1 style='margin-top: 0.5rem; font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #1e3a8a 0%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Vaultly</h1>
            <p style='color: #888; margin-top: 0.5rem; font-size: 0.9rem;'>Inventory Management System</p>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.info("👉 Please login or register to continue")


def login_page():
    """Display login page"""
    st.title("🔐 Login")
    
    with st.form("login_form"):
        username = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if username and password:
                user = User.authenticate(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = {
                        'id': str(user['_id']),
                        'username': user['username'],
                        'email': user['email'],
                        'role': user['role']
                    }
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            else:
                st.warning("⚠️ Please enter both username and password")


def register_page():
    """Display registration page"""
    st.title("📝 Register")
    
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        role = st.selectbox("Role", ["staff", "manager", "admin"])
        submit = st.form_submit_button("Register", use_container_width=True)
        
        if submit:
            if not all([username, email, password, confirm_password]):
                st.warning("⚠️ Please fill all fields")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters")
            else:
                user_id = User.create_user(username, email, password, role)
                if user_id:
                    # Auto-login after successful registration
                    user = User.authenticate(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = {
                            'id': str(user['_id']),
                            'username': user['username'],
                            'email': user['email'],
                            'role': user['role']
                        }
                        st.success("✅ Registration successful! Redirecting to dashboard...")
                        st.rerun()
                    else:
                        st.success("✅ Registration successful! Please login.")
                else:
                    st.error("❌ Username or email already exists")


def main_app():
    """Main application after authentication"""
    
    # Enhanced CSS for professional Zoho-style sidebar
    st.markdown("""
        <style>
            /* Dark sidebar background */
            [data-testid="stSidebar"] {
                background-color: #0f1419;
            }
            
            /* Hide default 'app' text and replace with 'Inventory' */
            [data-testid="stSidebarNav"]::before {
                content: "Inventory";
                display: block;
                text-align: center;
                font-size: 1.2rem;
                font-weight: 600;
                color: #e0e0e0;
                padding: 1rem 0.5rem;
                margin-bottom: 0.5rem;
                background-color: rgba(6, 182, 212, 0.08);
                border-radius: 8px;
                margin: 0.5rem;
            }
            
            /* Push navigation menu down to make room for logo */
            [data-testid="stSidebarNav"] {
                margin-top: 0rem;
                padding-top: 0rem;
                background-color: #0f1419;
            }
            
            /* Navigation list items */
            [data-testid="stSidebarNav"] ul {
                padding: 0;
            }
            
            [data-testid="stSidebarNav"] li {
                background-color: transparent !important;
                border-radius: 8px;
                margin: 3px 8px;
                transition: all 0.2s ease;
            }
            
            /* Hover effect */
            [data-testid="stSidebarNav"] li:hover {
                background-color: rgba(6, 182, 212, 0.12) !important;
            }
            
            /* Active page highlight */
            [data-testid="stSidebarNav"] li[aria-selected="true"] {
                background: linear-gradient(90deg, rgba(6, 182, 212, 0.2) 0%, rgba(6, 182, 212, 0.05) 100%) !important;
                border-left: 3px solid #06b6d4;
            }
            
            /* Navigation links */
            [data-testid="stSidebarNav"] a {
                color: #e0e0e0 !important;
                font-weight: 500;
                padding: 0.6rem 1rem;
            }
            
            [data-testid="stSidebarNav"] a:hover {
                color: #06b6d4 !important;
            }
            
            /* Active link */
            [data-testid="stSidebarNav"] li[aria-selected="true"] a {
                color: #06b6d4 !important;
                font-weight: 600;
            }
            
            /* User info card */
            .user-card {
                background: linear-gradient(135deg, #1e3a8a 0%, #06b6d4 100%);
                padding: 1rem;
                border-radius: 12px;
                margin: 1rem 0.5rem;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }
            
            .user-card h3 {
                color: white;
                margin: 0.5rem 0;
                font-size: 1.1rem;
                font-weight: 600;
            }
            
            .user-card p {
                color: rgba(255, 255, 255, 0.85);
                margin: 0.25rem 0;
                font-size: 0.85rem;
            }
            
            /* Sidebar buttons */
            .stButton button {
                background: linear-gradient(135deg, #1e3a8a 0%, #06b6d4 100%);
                color: white;
                border: none;
                font-weight: 600;
            }
            
            .stButton button:hover {
                background: linear-gradient(135deg, #06b6d4 0%, #1e3a8a 100%);
                box-shadow: 0 4px 8px rgba(6, 182, 212, 0.3);
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Display logo and text horizontally at the TOP (using st.logo to position at top)
    # Create horizontal layout with better proportions
    st.sidebar.markdown("""<div style='margin-top: -1rem;'></div>""", unsafe_allow_html=True)
    
    logo_col, text_col, spacer = st.sidebar.columns([1.2, 2.5, 0.3])
    
    with logo_col:
        st.image("static/vaultly_logo.png", width=65)
    
    with text_col:
        st.markdown("""
            <h2 style='margin: 0; margin-top: 20px; font-size: 1.9rem; font-weight: 700; background: linear-gradient(135deg, #1e3a8a 0%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Vaultly</h2>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # User info card
    st.sidebar.markdown(f"""
        <div class="user-card">
            <h3>👤 {st.session_state.user['username']}</h3>
            <p>🎭 {st.session_state.user['role'].title()}</p>
            <p>📧 {st.session_state.user['email']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Navigation info
    st.sidebar.markdown("""
        <div style='text-align: center; padding: 0.6rem; background-color: rgba(6, 182, 212, 0.08); border-radius: 8px; margin: 0.5rem; border: 1px solid rgba(6, 182, 212, 0.2);'>
            <p style='margin: 0; color: #06b6d4; font-size: 0.85rem; font-weight: 500;'>📍 Navigate using menu below</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Logout button
    if st.sidebar.button("🚪 Logout", use_container_width=True, type="primary"):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()
    
    # Main content
    st.title("🏠 Welcome to Vaultly")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", "0", "0")
    
    with col2:
        st.metric("Low Stock Items", "0", "0")
    
    with col3:
        st.metric("Total Value", "₹0", "0")
    
    with col4:
        st.metric("Total Bills", "0", "0")
    
    st.markdown("---")
    
    st.info("📊 Navigate to different pages using the sidebar to manage inventory, generate bills, chat with AI, and view analytics.")
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add Product", use_container_width=True):
            st.switch_page("pages/2_📦_Items.py")
    
    with col2:
        if st.button("📄 Create Bill", use_container_width=True):
            st.switch_page("pages/4_📄_Bills.py")
    
    with col3:
        if st.button("🤖 AI Chat", use_container_width=True):
            st.switch_page("pages/3_🤖_AI_Chat.py")


# Main application logic
if not st.session_state.authenticated:
    # Show auth sidebar
    show_auth_sidebar()
    
    # Show login/register tabs
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        login_page()
    
    with tab2:
        register_page()
else:
    main_app()

