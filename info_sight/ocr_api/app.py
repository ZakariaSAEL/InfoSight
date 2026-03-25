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
            primary_address = addresses[0].get("normalized", "") if addresses else ""
            coords = {"lat": 0.0, "lng": 0.0} # Geocoding hook
            
            # The frontend expects a flat structure + nested raw details
            formatted_res = {
                "id": str(uuid.uuid4()), # Generate a unique ID for IndexedDB
                "file_name": file.filename,
                "invoice_number": inv_data.get("invoice_number", "Unknown"),
                "date": inv_data.get("date", "Unknown"),
                "total": str(inv_data.get("total_amount", "0.00")),
                "vendor": inv_data.get("vendor_name", "Unknown"),
                "address": primary_address,
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
