
import streamlit as st
from datetime import datetime

def show():
    """Display the packages view"""
    st.title("📦 Packages")
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["All Packages", "Create Package"])
    
@st.dialog("Tracking Details")
def show_tracking_details(package, tracking_info):
    """Display tracking details in a dialog"""
    st.subheader(f"Tracking: {package.get('tracking_number', 'N/A')}")
    st.caption(f"Carrier: {package.get('carrier', 'Unknown')}")
    
    status_color = "green" if tracking_info['status'] == "Delivered" else "blue"
    st.markdown(f"### Status: :{status_color}[{tracking_info['status']}]")
    
    if tracking_info.get('is_mock'):
        st.warning("⚠️ Using mock data. Add `TRACKING_API_KEY` to .env for real updates.")
    
    st.markdown("### 🕒 History")
    for event in tracking_info.get('history', []):
        with st.container():
            c1, c2 = st.columns([1, 3])
            c1.caption(event['timestamp'])
            c2.write(f"**{event['status']}** - {event['details']}")
            st.divider()

def show():
    """Display the packages view"""
    st.title("📦 Packages")
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["All Packages", "Create Package"])
    
    with tab1:
        st.subheader("Package Tracking")
        
        from models.package import Package
        from services.tracking_service import TrackingService
        
        packages = Package.get_all_packages()
        
        if packages:
            # Metrics
            total = len(packages)
            delivered = sum(1 for p in packages if p['status'] == 'Delivered')
            transit = sum(1 for p in packages if p['status'] == 'In Transit')
            pending = total - delivered - transit
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Packages", total)
            col2.metric("In Transit", transit)
            col3.metric("Delivered", delivered)
            col4.metric("Pending", pending)
            
            st.markdown("---")
            
            # Package List
            for pkg in packages:
                tracking_num = pkg.get('tracking_number', 'N/A')
                carrier_name = pkg.get('carrier', 'Unknown')
                status_val = pkg.get('status', 'Unknown')
                
                if 'updated_at' in pkg:
                    updated_date = pkg['updated_at'].strftime('%Y-%m-%d')
                else:
                    updated_date = pkg.get('created_at', datetime.now()).strftime('%Y-%m-%d')
                    
                with st.expander(f"{carrier_name} - {tracking_num} ({status_val})"):
                    c1, c2, c3 = st.columns([2, 1, 1])
                    c1.write(f"**Destination:** {pkg.get('destination', 'N/A')}")
                    c2.caption(f"Updated: {updated_date}")
                    
                    if c3.button("🛰️ Track", key=f"track_{pkg['_id']}"):
                        try:
                            tracking_info = TrackingService.get_tracking_info(tracking_num, carrier_name)
                            show_tracking_details(pkg, tracking_info)
                        except Exception as e:
                            st.error(f"Tracking Error: {e}")
        else:
            st.info("No packages found. Add a package to start tracking.")
    
    with tab2:
        st.subheader("Create New Package")
        
        with st.form("create_package"):
            col1, col2 = st.columns(2)
            
            with col1:
                tracking_number = st.text_input("Tracking Number")
                carrier = st.selectbox("Carrier", ["FedEx", "UPS", "DHL", "USPS", "BlueDart", "Delhivery", "Other"])
                
            with col2:
                status = st.selectbox("Current Status", ["Pending", "In Transit", "Delivered", "Exception"])
                destination = st.text_input("Destination Address")
            
            notes = st.text_area("Notes")
            
            submit = st.form_submit_button("Add Package", type="primary", use_container_width=True)
            
            if submit:
                if not tracking_number:
                    st.error("Tracking Number is required")
                else:
                    from models.package import Package
                    try:
                        pkg_id = Package.create_package(
                            tracking_number=tracking_number,
                            carrier=carrier,
                            status=status,
                            destination=destination,
                            notes=notes,
                            created_by=st.session_state.user['id'] if st.session_state.user else None
                        )
                        if pkg_id:
                            st.toast("✅ Package Created Successfully!", icon="📦")
                            st.success(f"Package {tracking_number} added successfully!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error creating package: {e}")
