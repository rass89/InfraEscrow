import google.generativeai as genai
import json
import re

def analyze_infra_scan(image_file, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # We use a very strict prompt for JSON structure
    prompt = """
    You are an expert Structural Health Monitoring (SHM) Oracle. 
    Analyze the provided image of an infrastructure asset (e.g., dam, tunnel, road, bridge, or grid).
    1. Identify the asset type and component shown.
    2. Evaluate the structural integrity or repair quality.
    3. Determine if the maintenance meets professional engineering standards.
    Output ONLY a JSON object with these EXACT keys: 
    "asset_type", "status", "confidence", "details", "payout_authorized".
    Example: {"asset_type": "bridge", "status": "Verified", "confidence": "95%", "details": "No cracks", "payout_authorized": true}
    """
    
    img = genai.upload_file(image_file)
    response = model.generate_content([prompt, img])
    
    # --- BULLETPROOF PARSING ---
    try:
        # 1. Clean markdown backticks if Gemini adds them
        clean_text = re.sub(r'```json|```', '', response.text).strip()
        result = json.loads(clean_text)
    except Exception:
        # 2. Fallback if JSON is malformed
        result = {
            "asset_type": "Unknown",
            "status": "Rejected",
            "confidence": "N/A",
            "details": "AI response parsing failed. Check scan quality.",
            "payout_authorized": False
        }
    
    # 3. Ensure the 'confidence' key definitely exists even if AI missed it
    if "confidence" not in result:
        result["confidence"] = result.get("confidence_score", "N/A")
        
    return result




import google.generativeai as genai
import json
from PIL import Image

def analyze_infra_scan(image_file, api_key):
    """
    Uses the Gemini Multimodal API to analyze structural imagery.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        img = Image.open(image_file)

        prompt = """
        You are an expert Structural Health Monitoring (SHM) Oracle. 
        Analyze the provided image of an infrastructure asset (e.g., dam, tunnel, road, bridge, or grid). 
        
        1. Identify the asset type and component shown.
        2. Evaluate the structural integrity or repair quality.
        3. Determine if the maintenance meets professional engineering standards.

        Output strictly in JSON:
        {
        "asset_type": "string",
        "status": "Verified | Rejected",
        "confidence": "0-100%",
        "details": "Technical explanation of the verdict",
        "payout_authorized": true/false
        }
        """
        
        response = model.generate_content([prompt, img])
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean_text)
        return result

    except Exception as e:
        return {"status": "Failed", "confidence": 0.0, "details": f"API Error: {str(e)}"}