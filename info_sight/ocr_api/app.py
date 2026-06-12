from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
import datetime
from ocr_model import run_ocr

app = FastAPI(title="InfoSight OCR API", description="Local API for InfoSight document extraction")

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure a temp directory exists for intermediate file saving
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)


def select_primary_address(addresses: list) -> str:
    """Prefer customer/shipping addresses and ignore company/vendor addresses when possible."""
    if not isinstance(addresses, list) or not addresses:
        return ""

    preferred_roles = ("client", "customer", "shipping")
    for role in preferred_roles:
        for addr in addresses:
            if str(addr.get("role", "")).lower() == role:
                return str(addr.get("normalized", "")).strip()

    # Fallback: use the first non-vendor address if available.
    for addr in addresses:
        if str(addr.get("role", "")).lower() != "vendor":
            normalized = str(addr.get("normalized", "")).strip()
            if normalized:
                return normalized

    return str(addresses[0].get("normalized", "")).strip()


def extract_addresses_by_role(addresses: list) -> tuple:
    """
    Extracts (vendor_address, vendor_address_link, client_address, client_address_link) 
    from the list of extracted addresses based on role.
    """
    vendor_address = ""
    vendor_address_link = ""
    client_address = ""
    client_address_link = ""

    if not isinstance(addresses, list):
        return "", "", "", ""

    # Step 1: Strict role classification
    for addr in addresses:
        role = str(addr.get("role", "")).lower().strip()
        norm = str(addr.get("normalized", "")).strip()
        link = str(addr.get("maps_link", ""))
        
        if not norm:
            continue

        if role in ("vendor", "company", "issuer"):
            if not vendor_address:
                vendor_address = norm
                vendor_address_link = link
        elif role in ("client", "customer", "shipping", "recipient"):
            if not client_address:
                client_address = norm
                client_address_link = link

    # Step 2: Fallback logic for unclassified ("unknown") roles
    # If one of the addresses is still empty, assign unclassified addresses
    for addr in addresses:
        role = str(addr.get("role", "")).lower().strip()
        norm = str(addr.get("normalized", "")).strip()
        link = str(addr.get("maps_link", ""))

        if not norm:
            continue

        if role not in ("vendor", "company", "issuer", "client", "customer", "shipping", "recipient"):
            if not vendor_address and norm != client_address:
                vendor_address = norm
                vendor_address_link = link
            elif not client_address and norm != vendor_address:
                client_address = norm
                client_address_link = link

    return vendor_address, vendor_address_link, client_address, client_address_link


@app.post("/analyze")
async def analyze_endpoint(file: UploadFile = File(...)):
    """
    Receives an image file, processes it via Gemini 3 AI, and returns the extracted 
    structured JSON tailored for the React frontend's IndexedDB.
    """
    temp_path = os.path.join(TEMP_DIR, file.filename)
    
    try:
        # Save uploaded file temporarily
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Run AI extraction
        print(f"Processing {file.filename}...")
        ocr_data = run_ocr(temp_path)
        
        if "error" in ocr_data:
            return JSONResponse(status_code=500, content={"status": "error", "message": ocr_data["error"]})

        # Format the result nicely for the frontend IndexedDB schema
        try:
            inv_data = ocr_data.get("invoice_data", {})
            addresses = ocr_data.get("addresses", [])
            
            # Extract both addresses
            v_addr, v_link, c_addr, c_link = extract_addresses_by_role(addresses)
            
            # Use client address as primary fallback, else vendor address
            primary_address = c_addr if c_addr else (v_addr if v_addr else select_primary_address(addresses))
            
            customer_name = inv_data.get("client_name") or "Unknown"
            coords = {"lat": 0.0, "lng": 0.0} # Geocoding hook
            
            # The frontend expects a flat structure + nested raw details
            formatted_res = {
                "id": str(uuid.uuid4()), # Generate a unique ID for IndexedDB
                "file_name": file.filename,
                "invoice_number": inv_data.get("invoice_number", "Unknown"),
                "date": inv_data.get("date", "Unknown"),
                "total": str(inv_data.get("total_amount", "0.00")),
                "vendor": inv_data.get("vendor_name", "Unknown"),
                "customer_name": customer_name,
                "address": primary_address,
                "vendor_address": v_addr,
                "vendor_address_link": v_link,
                "client_address": c_addr,
                "client_address_link": c_link,
                "coordinates": coords,
                "raw_data": ocr_data,
                "confidence": ocr_data.get("confidence", {}), # To be added in ocr_model
                "created_at": datetime.datetime.now().isoformat()
            }
            return formatted_res
        except Exception as fmt_err:
            print(f"Formatting warning: {fmt_err}. Falling back to raw out.")
            return {"status": "success", "filename": file.filename, "data": ocr_data}
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
        
    finally:
        # Cleanup: remove the temporary file after processing
        if os.path.exists(temp_path):
            os.remove(temp_path)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

# Serve the React Frontend (SPA) if the static folder exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    
    # Custom 404 handler to support React Router pushing state natively
    @app.exception_handler(404)
    async def not_found(request, exc):
        return FileResponse(os.path.join(static_dir, "index.html"))
else:
    @app.get("/")
    def read_root():
        return {"message": "InfoSight V2 API is running. Send a POST request to /analyze to process an invoice."}
