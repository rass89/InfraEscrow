import google.generativeai as genai
import json
import re
from PIL import Image  # Add this import at the top!

def analyze_infra_scan(image_file, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = """
    Analyze this infrastructure image as a Structural Health Monitoring (SHM) expert to determine if a repair contractor should be paid. 
    Output ONLY a JSON object with these EXACT keys: 
    "asset_type", "status", "confidence", "details", "payout_authorized".

    CRITICAL BUSINESS LOGIC:
    1. If the structure is HEALTHY, MAINTAINED, or PROPERLY REPAIRED (no severe damage):
       -> Set "status" to "Verified" and "payout_authorized" to true.
    2. If the structure is DAMAGED, FAILING, CRACKED, LEANING, or DANGEROUS:
       -> Set "status" to "Rejected" and "payout_authorized" to false.

    Example (Healthy): {"asset_type": "steel bridge", "status": "Verified", "confidence": "95%", "details": "Clean structural lines, no rust.", "payout_authorized": true}
    Example (Damaged): {"asset_type": "concrete building", "status": "Rejected", "confidence": "99%", "details": "Severe leaning and spalling.", "payout_authorized": false}
    """
    
    # --- THE FIX ---
    # Open the Streamlit memory file as a PIL Image
    img = Image.open(image_file)
    
    # Pass the PIL Image directly to Gemini (no upload_file needed!)
    response = model.generate_content([prompt, img])
    
    # --- BULLETPROOF PARSING ---
    try:
        clean_text = re.sub(r'```json|```', '', response.text).strip()
        result = json.loads(clean_text)
    except Exception:
        result = {
            "asset_type": "Unknown",
            "status": "Rejected",
            "confidence": "N/A",
            "details": "AI response parsing failed. Check scan quality.",
            "payout_authorized": False
        }
    
    if "confidence" not in result:
        result["confidence"] = result.get("confidence_score", "N/A")
    return result    
        
