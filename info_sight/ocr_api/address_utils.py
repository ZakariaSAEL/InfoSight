import re
import urllib.parse

# Common abbreviations to normalize
NORM_RULES = {
    r'\bBD\b': 'Boulevard',
    r'\bBD.\b': 'Boulevard',
    r'\bBOUL\b': 'Boulevard',
    r'\bBOUL.\b': 'Boulevard',
    r'\bAV\b': 'Avenue',
    r'\bAV.\b': 'Avenue',
    r'\bST\b': 'Street',
    r'\bST.\b': 'Street',
    r'\bRTE\b': 'Route',
    r'\bRTE.\b': 'Route',
    r'\bAPP\b': 'Appartement',
    r'\bNR\b': 'Numéro',
    r'\bN°\b': 'Numéro',
}

STOP_WORDS = [
    "invoice", "date", "due", "client", "cllent", "billed", "facture", "nom", "article", 
    "contact", "autre", "tel", "tél", "email", "description", "amount", "total", "net"
]

def preprocess_text_for_addresses(text: str) -> str:
    """
    Removes common key-value pairs (like Date, Invoice #) that often interrupt 
    multi-line addresses in OCR output.
    """
    # 1. Dates: Month DD, YYYY or DD/MM/YYYY
    month_names = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'
    date_pattern1 = rf'{month_names}\s+\d{{1,2}}\s*,\s*\d{{4}}'
    date_pattern2 = r'\b\d{{1,2}}[/-]\d{{1,2}}[/-]\d{{2,4}}\b'
    
    text = re.sub(date_pattern1, ' ', text, flags=re.IGNORECASE)
    text = re.sub(date_pattern2, ' ', text, flags=re.IGNORECASE)
    
    # 2. Key names like Invoice Date:, Due Date:, Invoice #:, etc.
    noise_keys = [
        r'\bInvoice\s*(?:Date|No|Number|#)?[.\s#:]*(?:AD-)?\d+(?:-\d+)*\b',
        r'\bDue\s*Date[.\s:]*',
        r'\bInvoice\s*Date[.\s:]*',
        r'\bFacture\s*(?:#|N°|No)?\s*\d+\b',
        r'\bDate\s*(?:of\s*invoice)?[.\s:]*',
    ]
    
    for nk in noise_keys:
        text = re.sub(nk, ' ', text, flags=re.IGNORECASE)
        
    # Replace multiple spaces with a single space to close the gap
    return re.sub(r'\s+', ' ', text).strip()

def clean_extracted_address(addr: str) -> str:
    """
    Trims the extracted address at the first occurrence of common non-address words.
    """
    lower_addr = addr.lower()
    min_idx = len(addr)
    for sw in STOP_WORDS:
        match = re.search(r'\b' + sw + r'\b', lower_addr)
        if match:
            idx = match.start()
            if 0 < idx < min_idx:
                min_idx = idx
    # Drop any trailing punctuation that might be left
    return addr[:min_idx].strip().strip(" ,;-:")

def normalize_address(text: str):
    """
    Replaces abbreviations with full words based on NORM_RULES.
    """
    normalized = text
    for pattern, replacement in NORM_RULES.items():
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
    return normalized

def extract_addresses(text: str):
    """
    Finds potential address blocks.
    Prioritizes text following keywords 'adresse' or 'address'.
    """
    found_addresses = []
    
    text = preprocess_text_for_addresses(text)
    
    # 1. Keyword-based heuristic (User suggested)
    # Look for "Adresse :" or "Address :" and capture everything until a newline or long break
    keyword_pattern = r'(?:adresse|address)\s*[:\-]?\s*(.*?(?:\n|$))'
    keyword_matches = re.findall(keyword_pattern, text, flags=re.IGNORECASE)
    for match in keyword_matches:
        clean_match = clean_extracted_address(match.strip())
        if len(clean_match) > 5: # Filter out very short noise
            found_addresses.append(clean_match)
            
    # 2. Generic street patterns (Fallback/Additional)
    # Look for patterns like "123 Bd Anfa, Casablanca"
    # Negative lookbehind to avoid matching invoice numbers (e.g. -0015)
    street_pattern = r'(?<![-/#_])\b(\d{1,5}\b[\w\s,;]{1,30}?(?:Boulevard|Avenue|Rue|Route|Street|Bd|Av|St|Rte|Blvd)\b[\w\s,;]{1,60})'
    norm_text = normalize_address(text)
    street_matches = re.finditer(street_pattern, norm_text, flags=re.IGNORECASE)
    for match in street_matches:
        raw_addr = match.group(1).strip()
        cleaned_addr = clean_extracted_address(raw_addr)
        
        # Remove partial trailing words that might have been cut off by the 40 char limit
        cleaned_addr = re.sub(r'\s+\w{1,3}$', '', cleaned_addr).strip(" ,;-:")
        
        if len(cleaned_addr) > 5 and cleaned_addr not in found_addresses:
            found_addresses.append(cleaned_addr)
            
    # Return unique matches
    return list(set(found_addresses))

def generate_google_maps_link(address: str):
    """
    Creates a Google Maps search URL for the given address.
    """
    base_url = "https://www.google.com/maps/search/?api=1&query="
    encoded_address = urllib.parse.quote(address)
    return base_url + encoded_address

if __name__ == "__main__":
    test_text = """
    FACTURE #98765
    Nom: Client Alpha
    Adresse : 45 Rue de la Liberté, Casablanca, Maroc
    Article: PC Portable - 5000 DH
    Contact: Address: 12 bis Boulevard des FAR, Tanger
    Autre: 123 BD Anfa, Casablanca
    """
    print("--- Normalization ---")
    print(normalize_address(test_text))
    
    print("\n--- Extraction ---")
    addresses = extract_addresses(test_text)
    for addr in addresses:
        print(f"Address: {addr}")
        print(f"Maps: {generate_google_maps_link(addr)}\n")
