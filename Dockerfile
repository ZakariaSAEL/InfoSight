# Use Python 3.10 or higher
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for PyMuPDF/Pillow)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY info_sight/ocr_api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose ports for Streamlit and FastAPI
EXPOSE 8501
EXPOSE 8000

# Set environment variables (GEMINI_API_KEY should be provided at runtime)
ENV PYTHONUNBUFFERED=1

# Command to run (defaults to Streamlit, but can be overridden)
CMD ["streamlit", "run", "info_sight/ocr_api/ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
