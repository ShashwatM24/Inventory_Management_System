
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_service import get_full_business_context

print("Verifying fix for get_full_business_context...")
try:
    context = get_full_business_context()
    if "Error assembling business context" in context:
        print("FAIL: Still getting error message:")
        print(context)
        exit(1)
    else:
        print("SUCCESS: Context generated safely!")
        print(f"Context length: {len(context)}")
        # Check if we have product entries
        if "PRODUCT CATALOG" in context:
            print("Product catalog present.")
        exit(0)
except Exception as e:
    print(f"CRITICAL FAIL: Exception raised: {e}")
    exit(1)
