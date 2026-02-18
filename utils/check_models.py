import os
import google.generativeai as genai

# Debug .env content
print("Debugging .env file...")
api_key = None
try:
    with open(".env", "r", encoding="utf-8") as f:
        lines = f.readlines()
        print(f"Found {len(lines)} lines in .env")
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                
                # Mask value for security
                masked_value = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "****"
                print(f"Line {i+1}: Found key '{key}'")
                
                if key == "GEMINI_API_KEY":
                    api_key = value
                    print(f"--> SUCCESS: GEMINI_API_KEY found!")

except Exception as e:
    print(f"Error reading .env: {e}")

if not api_key:
    # Try environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print("Found GEMINI_API_KEY in environment variables")

if not api_key:
    print("❌ FAILURE: No API key found in .env or environment")
else:
    # Configure Gemini
    genai.configure(api_key=api_key)
    try:
        print(f"\n✅ Authenticating with key: {api_key[:4]}...")
        print("Listing available models that support generateContent:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"❌ Error listing models: {e}")
