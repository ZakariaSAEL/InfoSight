import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found")
else:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("Available Models:")
    try:
        models = client.models.list()
        for model in models:
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")
