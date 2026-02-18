
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found.")
    exit(1)

genai.configure(api_key=api_key)

try:
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if not models:
        print("Error: No models found.")
        exit(1)
        
    print(f"Available models: {models}")
    
    # Select best model
    best_model = None
    
    # 1. Try generic names
    priority_list = [
        'models/gemini-1.5-flash',
        'models/gemini-1.5-flash-latest',
        'models/gemini-1.5-pro',
        'models/gemini-pro'
    ]
    
    for p in priority_list:
        if p in models:
            best_model = p
            break
    
    # 2. Try partial match for flash
    if not best_model:
        for m in models:
            if 'flash' in m.lower():
                best_model = m
                break
                
    # 3. Try partial match for pro
    if not best_model:
        for m in models:
            if 'pro' in m.lower():
                best_model = m
                break
                
    # 4. Fallback to first available
    if not best_model:
        best_model = models[0]
        
    print(f"Selected model: {best_model}")
    
    # Strip 'models/' prefix if library version expects it (but 0.8.6 usually handles both, let's keep it safe)
    # Actually, recent libs handle 'models/' or just name. But 'gemini-1.5-flash' usually works.
    # However, if 'models/gemini-1.5-flash' is returned by list_models, we can use that.
    
    # Just use the name as returned by list_models
    model_name_to_use = best_model
    if model_name_to_use.startswith("models/"):
        model_name_to_use = model_name_to_use.replace("models/", "")

    print(f"Using model name: {model_name_to_use}")
    
    # Update services/ai_service.py
    file_path = 'services/ai_service.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We look for: model = genai.GenerativeModel('...')
    # We'll replace the hardcoded string
    import re
    new_content = re.sub(
        r"genai\.GenerativeModel\(['\"][\w\.-]+['\"]\)", 
        f"genai.GenerativeModel('{model_name_to_use}')", 
        content
    )
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated services/ai_service.py")
    else:
        print("No changes needed or regex failed.")

except Exception as e:
    print(f"Error fixing model: {e}")
