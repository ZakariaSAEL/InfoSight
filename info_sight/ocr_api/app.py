from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
from ocr_model import run_ocr

app = FastAPI(title="InfoSight OCR API", description="Local API for GLM-OCR document extraction")

# Ensure a temp directory exists for intermediate file saving
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    """
    Receives an image file, processes it via GLM-OCR, and returns the extracted text.
    """
    temp_path = os.path.join(TEMP_DIR, file.filename)
    
    try:
        # Save uploaded file temporarily
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Run OCR extraction
        print(f"Processing {file.filename}...")
        ocr_data = run_ocr(temp_path)
        
        if "error" in ocr_data:
            return JSONResponse(status_code=500, content={"status": "error", "message": ocr_data["error"]})

        return {
            "status": "success",
            "filename": file.filename,
            "data": ocr_data
        }
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
        
    finally:
        # Cleanup: remove the temporary file after processing
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/")
def read_root():
    return {"message": "InfoSight OCR API is running. Send a POST request to /ocr to analyze an image."}
