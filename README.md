# 🔍 InfoSight - Smart Multilingual OCR

InfoSight is a powerful, modern OCR application designed to extract structured data from invoices and documents. It leverages **Google Gemini 3** to provide state-of-the-art accuracy across multiple languages, including **Arabic (RTL support)**, **French**, and **English**.

## ✨ Key Features

- **Multilingual OCR**: Native support for Arabic, French, and English text extraction.
- **Smart Normalization**: Automatically standardizes messy Moroccan addresses (expanding abbreviations like `Bd`, `Res`, `App`, etc.).
- **Interactive UI**: A sleek, user-friendly interface built with Streamlit.
- **FastAPI Backend**: A robust REST API for integrating OCR into other applications.
- **Cloud Ready**: Includes a `Dockerfile` and deployment guide for easy hosting.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- A Google Gemini API Key (get one at [aistudio.google.com](https://aistudio.google.com/app/apikey))

### 2. Installation
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r info_sight/ocr_api/requirements.txt
   ```
3. Create a `.env` file in `info_sight/ocr_api/` and add your key:
   ```env
   GEMINI_API_KEY=your_key_here
   ```

### 3. Launching the App
For your convenience, I've created two startup scripts in the root directory:
- **`start_website.bat`**: Launches both the **UI (8501)** and the **API (8000)**.
- **`start_ui.bat`**: Launches only the Streamlit UI.

Alternatively, run manually:
```bash
streamlit run info_sight/ocr_api/ui.py
```

## 🛠 Tech Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI & Uvicorn
- **AI Model**: Google Gemini 3 Flash Preview
- **OCR Engine**: Multimodal Gemini In-Context Learning
- **PDF Processing**: PyMuPDF (fitz)

## ☁️ Cloud Deployment
Refer to the `deployment_guide.md` for instructions on hosting this app on AWS, Heroku, or Streamlit Cloud. A `Dockerfile` is also provided in the root.

---
*Created for Projet PFE - 2026*
