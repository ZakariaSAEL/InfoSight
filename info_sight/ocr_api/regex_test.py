import re

text = "Aapex Digital INVOICE Solutions Invoice #: AD-2024-0015 145 Main Street Suite 300 Invoice Date: October 26, 2024 San Francisco; CA 94105 Due Date: November 10, 2024 Cllent: Billed To: Greenlignt Innovations Sarah Chen 888 Silicon Valley Blvd Palo Ato, CA 94304 description Unit Price"

text2 = "FACTURE #98765 Nom: Client Alpha Adresse : 45 Rue de la Liberté, Casablanca, Maroc Article: PC Portable - 5000 DH Contact: Address: 12 bis Boulevard des FAR, Tanger Autre: 123 BD Anfa, Casablanca"

def preprocess_text_for_addresses(t: str) -> str:
    # Remove common key-value pairs that interrupt addresses
    # e.g., Invoice #: AD-2024-0015
    # e.g., Invoice Date: October 26, 2024
    # e.g., Due Date: November 10, 2024
    
    # 1. Dates: Month DD, YYYY or DD/MM/YYYY
    month_names = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
    date_pattern1 = rf'{month_names}\s+\d{{1,2}}\s*,\s*\d{{4}}'
    date_pattern2 = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
    
    # Replace these dates first
    t = re.sub(date_pattern1, '', t, flags=re.IGNORECASE)
    t = re.sub(date_pattern2, '', t, flags=re.IGNORECASE)
    
    # 2. Key names like Invoice Date:, Due Date:, Invoice #:, etc.
    noise_keys = [
        r'Invoice\s*(?:Date|No|Number|#)?[.\s#:]*(?:AD-)?\d+(?:-\d+)*', # e.g. Invoice #: AD-2024-0015 
        r'Due\s*Date[.\s:]*',
        r'Invoice\s*Date[.\s:]*',
        r'Facture\s*(?:#|N°|No)?\s*\d+',
        r'Date\s*(?:of\s*invoice)?[.\s:]*',
    ]
    
    for nk in noise_keys:
        t = re.sub(nk, ' ', t, flags=re.IGNORECASE)
        
    # Replace multiple spaces with a single space to close the gap
    t = re.sub(r'\s+', ' ', t).strip()
    return t

print("--- Original ---")
print(text)
print("\n--- Preprocessed ---")
clean_t = preprocess_text_for_addresses(text)
print(clean_t)

print("\n--- Testing Address Extraction on Preprocessed ---")

STOP_WORDS = [
    "invoice", "date", "due", "client", "billed", "facture", "nom", "article", 
    "contact", "autre", "tel", "tél", "email", "description", "amount", "total", "net"
]

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
    return addr[:min_idx].strip().strip(" ,;-:")

street_pattern = r'(?<![-/#_])\b(\d{1,5}\b[\w\s,;]{1,30}?(?:Boulevard|Avenue|Rue|Route|Street|Bd|Av|St|Rte|Blvd)\b[\w\s,;]{1,60})'
for m in re.finditer(street_pattern, clean_t, flags=re.IGNORECASE):
    raw_addr = m.group(1).strip()
    cleaned_addr = clean_extracted_address(raw_addr)
    cleaned_addr = re.sub(r'\s+\w{1,3}$', '', cleaned_addr).strip(" ,;-:")
    print("Extracted:", cleaned_addr)

