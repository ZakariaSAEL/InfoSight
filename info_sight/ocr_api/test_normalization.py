import os
from ocr_model import run_ocr
import json

def test_complex_invoice():
    image_path = 'complex_test_invoice.png'
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found")
        return

    print(f"Testing OCR on {image_path}...")
    results = run_ocr(image_path)
    
    if "error" in results:
        print(f"OCR Error: {results['error']}")
    else:
        print("--- Extraction Results ---")
        print(json.dumps(results, indent=2))
        
        print("\n--- Normalization Verification ---")
        if "addresses" in results:
            for addr in results["addresses"]:
                print(f"Original:   {addr.get('original')}")
                print(f"Normalized: {addr.get('normalized')}")
                print("-" * 20)

if __name__ == "__main__":
    test_complex_invoice()
