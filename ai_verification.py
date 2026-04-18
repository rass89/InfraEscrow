import google.generativeai as genai
import json
from PIL import Image

def analyze_bridge_scan(image_file, api_key):
    """
    Uses the Gemini Multimodal API to analyze structural imagery.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        img = Image.open(image_file)

        prompt = """
        You are an expert Structural Health Monitoring (SHM) Oracle. Analyze the provided image of an infrastructure asset (e.g., concrete dam, steel joint, asphalt road, or tunnel lining).

        Your Task:

        Identify the material and the probable infrastructure component.

        Evaluate the repair or maintenance quality against professional engineering standards.

        Look for critical failure indicators: cracks, spalling, corrosion, or structural deformation.

        Output strictly in JSON:
        {
        'asset_type': 'string',
        'status': 'Verified | Rejected',
        'confidence_score': 0.0-1.0,
        'engineering_notes': 'short technical summary',
        'payout_authorized': true/false
        }
        """
        
        response = model.generate_content([prompt, img])
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean_text)
        return result

    except Exception as e:
        return {"status": "Failed", "confidence": 0.0, "details": f"API Error: {str(e)}"}