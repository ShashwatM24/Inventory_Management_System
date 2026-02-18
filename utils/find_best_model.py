
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("NO_KEY")
    exit(1)

genai.configure(api_key=api_key)

try:
    all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # Priority list
    priorities = [
        'models/gemini-1.5-flash',
        'models/gemini-1.5-flash-latest',
        'models/gemini-1.5-pro',
        'models/gemini-1.5-pro-latest',
        'models/gemini-pro'
    ]
    
    found = None
    for p in priorities:
        if p in all_models:
            found = p
            break
            
    if found:
        print(found)
    elif all_models:
        print(all_models[0])
    else:
        print("NO_MODELS")
        
except Exception as e:
    print(f"ERROR: {e}")
