
"""
Tracking Service for handling carrier API integrations
Supports 17TRACK (Real Implementation) and EasyPost (Mock)
"""
import requests
import os
import random
import json
from datetime import datetime

class TrackingService:
    """Service to handle package tracking"""
    
    API_KEY = os.getenv("TRACKING_API_KEY", "")
    PROVIDER = os.getenv("TRACKING_PROVIDER", "17TRACK")
    
    @staticmethod
    def get_tracking_info(tracking_number, carrier):
        """
        Get tracking information for a package
        Returns a dict with status and history
        """
        if not TrackingService.API_KEY or TrackingService.API_KEY == "mock_key":
            return TrackingService._get_mock_data(tracking_number, carrier)
            
        if TrackingService.PROVIDER == "17TRACK":
            return TrackingService._get_17track_data(tracking_number, carrier)
            
        return TrackingService._get_mock_data(tracking_number, carrier)

    @staticmethod
    def _get_17track_data(tracking_number, carrier):
        """
        Fetch real tracking data from 17TRACK API v2.4
        Docs: https://api.17track.net/en/doc/v2/4
        """
        url = "https://api.17track.net/track/v2.2/gettrackinfo"
        headers = {
            "17token": TrackingService.API_KEY,
            "Content-Type": "application/json"
        }
        
        # 17TRACK requires a list of items. We only query one.
        payload = [
            {
                "number": tracking_number
            }
        ]
        
        # If carrier is known, we can add it, but 17TRACK auto-detects nicely.
        # payload[0]["carrier"] = _map_carrier_code(carrier) 
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()
            
            if data['code'] == 0:
                # Success - Check if accepted
                accepted = data['data'].get('accepted', [])
                rejected = data['data'].get('rejected', [])
                
                if accepted:
                    track_info = accepted[0]['track']
                    
                    # Map 17TRACK status to our status
                    # 0:Not Found, 10:Transit, 20:Expired, 30:Ready, 35:Out for Delivery, 
                    # 40:Failed Attempt, 50:Delivered, 60:Exception
                    status_map = {
                        0: "Not Found",
                        10: "In Transit",
                        20: "Expired",
                        30: "Ready for Pickup",
                        35: "Out for Delivery",
                        40: "Delivery Failed",
                        50: "Delivered",
                        60: "Exception"
                    }
                    
                    current_status_code = track_info['z0']['z']
                    current_status = status_map.get(current_status_code, "Unknown")
                    
                    # Events history
                    events = []
                    # z1 is the list of events (latest first usually, or we sort)
                    raw_events = track_info.get('z1', [])
                    for e in raw_events:
                        events.append({
                            "timestamp": e.get('a', ''), # Time
                            "status": e.get('z', ''),    # Status description
                            "location": e.get('c', '') + ", " + e.get('d', ''), # Location
                            "details": e.get('z', '')
                        })
                    
                    return {
                        "tracking_number": tracking_number,
                        "carrier": carrier,
                        "status": current_status,
                        "estimated_delivery": track_info.get('z0', {}).get('e', 'N/A'),
                        "history": events,
                        "is_mock": False
                    }
                elif rejected:
                    # Number was rejected by 17TRACK (e.g. invalid number, carrier not supported, duplicates etc)
                    error_msg = rejected[0].get('message', 'Tracking number rejected by carrier')
                    return {
                        "tracking_number": tracking_number,
                        "carrier": carrier,
                        "status": "Rejected/Invalid",
                        "estimated_delivery": "N/A",
                        "history": [{"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "status": "Error", "details": f"17TRACK Error: {error_msg}"}],
                        "is_mock": False
                    }
                else:
                    return {
                        "tracking_number": tracking_number,
                        "carrier": carrier,
                        "status": "No Info Available",
                        "estimated_delivery": "N/A",
                        "history": [{"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "status": "Info", "details": "Tracking number accepted but no data yet."}],
                        "is_mock": False
                    }
            else:
                # API Error or No Data (e.g. number not registered yet)
                return {
                    "tracking_number": tracking_number,
                    "carrier": carrier,
                    "status": "API Error",
                    "estimated_delivery": "N/A",
                    "history": [{"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "status": "Error", "details": data.get('message', 'Unknown API Error')}],
                    "is_mock": False
                }
                
        except Exception as e:
            return {
                "tracking_number": tracking_number,
                "carrier": carrier,
                "status": "Connection Error",
                "estimated_delivery": "N/A",
                "history": [{"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "status": "Error", "details": str(e)}],
                "is_mock": False
            }

    @staticmethod
    def _get_mock_data(tracking_number, carrier):
        """Generate realistic mock tracking data"""
        statuses = ["In Transit", "Out for Delivery", "Delivered", "Exception", "Pending"]
        locations = ["New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Miami, FL"]
        
        current_status = "In Transit" # Default
        if "DEL" in tracking_number: current_status = "Delivered"
        
        random.seed(tracking_number)
        
        history = []
        for i in range(3):
            history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": random.choice(statuses),
                "location": random.choice(locations),
                "details": f"Package processed at {random.choice(locations)} facility"
            })
            
        return {
            "tracking_number": tracking_number,
            "carrier": carrier,
            "status": current_status,
            "estimated_delivery": datetime.now().strftime("%Y-%m-%d"),
            "history": history,
            "is_mock": True
        }
