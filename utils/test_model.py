
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

try:
    # Read the model name from ai_service.py to test exactly what we set
    with open('services/ai_service.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    match = re.search(r"genai\.GenerativeModel\(['\"]([\w\.-]+)['\"]\)", content)
    if match:
        model_name = match.group(1)
        print(f"Testing model: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print(f"Success! Response: {response.text}")
    else:
        print("Could not find model name in ai_service.py")
        
except Exception as e:
    print(f"Failed: {e}")
