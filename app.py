
"""
Main Streamlit Application - Inventory Management System
Single Page Application (SPA) styling for seamless transitions
"""
import streamlit as st

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Vaultly - Inventory Management",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import dependencies
from models.user import User
from config.database import init_db

# Import views
import views.dashboard as dashboard
import views.inventory as inventory
import views.chat as chat
import views.bills as bills
import views.reports as reports
import views.sales_orders as sales_orders
import views.packages as packages
import views.invoices as invoices
import views.purchase_orders as purchase_orders

# Initialize database
try:
    init_db()
except Exception as e:
    st.error(f"Failed to connect to database: {e}")
    st.stop()

# Initialize session state for authentication and navigation
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

# CSS for styling
def local_css():
    st.markdown("""
        <style>
            /* Dark sidebar background */
            [data-testid="stSidebar"] {
                background-color: #0f1419;
            }
            
            /* Custom Button Styling to look like Nav Links */
            div.stButton > button {
                width: 100%;
                background-color: transparent;
                color: #e0e0e0;
                border: none;
                text-align: left;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                transition: all 0.2s ease;
            }
            
            div.stButton > button:hover {
                background-color: rgba(6, 182, 212, 0.12);
                color: #06b6d4;
                border: none;
            }
            
            div.stButton > button:focus {
                background-color: rgba(6, 182, 212, 0.12);
                color: #06b6d4;
                border: none;
                box-shadow: none;
            }

            /* Main content padding */
            .main .block-container {
                padding-top: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)


def show_auth_sidebar():
    """Display minimal sidebar for login/register pages"""
    local_css()
    
    # Center and display logo image
    col1, col2, col3 = st.sidebar.columns([1, 2, 1])
    with col2:
        try:
            st.image("static/vaultly_logo.png", use_container_width=True)
        except:
            st.header("🔐")
    
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


def sidebar_navigation():
    """Render the sidebar navigation"""
    with st.sidebar:
        # Logo and Title
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                st.image("static/vaultly_logo.png", use_container_width=True)
            except:
                st.header("🔐")
        
        st.markdown("<h3 style='text-align: center; color: #06b6d4;'>Vaultly</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Navigation Buttons
        pages = {
            "Dashboard": "🏠 Dashboard",
            "Inventory": "📦 Items",
            "AI Chat": "🤖 AI Chat",
            "Bills": "📄 Bills",
            "Reports": "📊 Reports",
            "Sales Orders": "🛒 Sales Orders",
            "Packages": "📦 Packages",
            "Invoices": "📝 Invoices",
            "Purchase Orders": "🛍️ Purchase Orders"
        }
        
        for page_key, page_label in pages.items():
            # Highlight active page button using session state logic or conditional styling
            # Using standard button logic for SPA
            if st.button(page_label, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun() # Rerun to update the main view
        
        st.markdown("---")
        
        # Clear Chat History (Only on AI Chat page)
        if st.session_state.get('current_page') == "AI Chat":
             if st.button("🗑️ Clear Chat History", key="clear_chat_nav", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
             # Optional: Add another separator if desired, but "---" is already above. 
        
        # Logout Button
        if st.button("🚪 Logout", key="logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.current_page = "Dashboard"
            st.rerun()


def main_app():
    """Main application Logic"""
    local_css()
    sidebar_navigation()
    
    # Routing Logic
    page = st.session_state.current_page
    
    if page == "Dashboard":
        dashboard.show()
    elif page == "Inventory":
        inventory.show()
    elif page == "AI Chat":
        chat.show()
    elif page == "Bills":
        bills.show()
    elif page == "Reports":
        reports.show()
    elif page == "Sales Orders":
        sales_orders.show()
    elif page == "Packages":
        packages.show()
    elif page == "Invoices":
        invoices.show()
    elif page == "Purchase Orders":
        purchase_orders.show()
    else:
        dashboard.show() # Fallback


# Application entry point
if not st.session_state.authenticated:
    show_auth_sidebar()
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        login_page()
    with tab2:
        register_page()
else:
    main_app()
