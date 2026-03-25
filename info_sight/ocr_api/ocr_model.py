import os
import io
from PIL import Image
import fitz  # PyMuPDF
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from address_utils import generate_google_maps_link

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

def extract_invoice_data_with_gemini(pil_images: list) -> dict:
    """Sends one or multiple PIL images to Gemini and returns extracted structured invoice data."""
    if not GEMINI_API_KEY:
        return {"error": "GEMINI_API_KEY is not set. Please get a free API key at https://aistudio.google.com/app/apikey and add it to your .env file."}
        
    try:
        prompt = """
You are an expert OCR and data extraction AI. Extract the information from this invoice document and return it ONLY as a valid JSON object. Do not include any formatting like ` ```json ` blocks, just output the raw JSON string.

The JSON object MUST contain the following keys exactly:
- "text": The complete raw text extracted from the document.
- "invoice_data": An object containing the following keys (if a field is not found, set its value to null):
  - "invoice_number": The invoice identifier
  - "date": The invoice date (format as YYYY-MM-DD ideally)
  - "total_amount": The total amount or grand total
  - "vendor_name": The name of the company issuing the invoice
  - "client_name": The name of the client being billed
- "confidence": An object providing a confidence score (from 0.0 to 1.0) for each extracted field in "invoice_data". Keys must match the "invoice_data" keys exactly. Use 1.0 for high certainty, lower for ambiguous/unclear text.
- "addresses": A list of address objects found in the document. For each address, provide:
  - "role": e.g., "vendor", "client", "shipping", or "unknown"
  - "original": The exact address text found in the document
  - "normalized": The normalized Moroccan address. RULES for normalization: Expand abbreviations: 'BD', 'Bd', 'bd', 'Bvd' to 'Boulevard'; 'Av', 'AV' to 'Avenue'; 'St' to 'Street'; 'Rte' to 'Route'; 'Lot.', 'Lot' to 'Lotissement'; 'Res.', 'Res' to 'Résidence'; 'Imm.', 'Imm' to 'Immeuble'; 'App', 'Appt' to 'Appartement'; 'Qrt' to 'Quartier'; 'Z.I.' to 'Zone Industrielle'. Ensure correct capitalization (e.g., 'boulevard' -> 'Boulevard'). Join multi-line addresses into a single clean line.
- IMPORTANT: For Arabic text, ensure the character order is logically correct (Right-to-Left) and remains consistent even when mixed with Latin text. Do not reverse words or characters; maintain the natural reading order.
"""
        contents = [prompt] + pil_images
        
        print("Waiting for Google Gemini response...")
        # Use gemini-3-flash-preview as requested by the user
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        
        content = response.text.strip()
        if not content:
            return {"error": "Empty response from Gemini"}
            
        return json.loads(content)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return {"error": "API Rate Limit Peak: The Gemini Free Tier limit was reached. Please wait 10-20 seconds and try again. The fix is to wait for the quota reset."}
        print(f"Error calling Gemini: {e}")
        return {"error": error_msg}

def run_ocr(file_path: str):
    """
    Runs OCR on the given image or PDF using Zhipu AI GLM-4V.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        pil_images = []
        
        if ext == '.pdf':
            print(f"Processing PDF: {file_path}")
            doc = fitz.open(file_path)
            for page_index in range(len(doc)):
                page = doc.load_page(page_index)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                print(f"  Loaded page {page_index + 1}/{len(doc)}")
                pil_images.append(img)
            doc.close()
        else:
            print(f"Processing Image: {file_path}...")
            pil_images.append(Image.open(file_path))
            
        print("Extracting structured data via Gemini...")
        extracted_data = extract_invoice_data_with_gemini(pil_images)
        
        if "error" in extracted_data:
            return {"error": extracted_data["error"]}
            
        # Add google maps links to the addresses
        if "addresses" in extracted_data and isinstance(extracted_data["addresses"], list):
            for addr_obj in extracted_data["addresses"]:
                if "normalized" in addr_obj and addr_obj["normalized"]:
                    addr_obj["maps_link"] = generate_google_maps_link(addr_obj["normalized"])
        
        return extracted_data
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Test locally
    test_path = "test_invoice.png"
    if os.path.exists(test_path):
        print(f"Testing OCR on {test_path}...")
        print("Result:", run_ocr(test_path))
    else:
        print("No test image found for local test.")
