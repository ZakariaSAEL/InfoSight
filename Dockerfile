# ==========================================
# Stage 1: Build React Frontend
# ==========================================
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY info_sight/frontend/package*.json ./
RUN npm install

# Copy all frontend source files and build
COPY info_sight/frontend/ ./
RUN npm run build


# ==========================================
# Stage 2: Build FastAPI Backend & Serve SPA
# ==========================================
FROM python:3.10-slim
WORKDIR /app

# Install system dependencies required for PyMuPDF/Pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY info_sight/ocr_api/requirements.txt ./info_sight/ocr_api/
RUN pip install --no-cache-dir -r info_sight/ocr_api/requirements.txt

# Copy backend code
COPY info_sight/ocr_api/ ./info_sight/ocr_api/

# Copy React build from Stage 1 into the backend's static folder
COPY --from=frontend-builder /app/frontend/dist ./info_sight/ocr_api/static

# Expose single port
EXPOSE 8000

# Set environment variables (GEMINI_API_KEY must be passed at runtime)
ENV PYTHONUNBUFFERED=1

# Run Uvicorn and specify the app directory so it finds local python modules
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "info_sight/ocr_api"]
