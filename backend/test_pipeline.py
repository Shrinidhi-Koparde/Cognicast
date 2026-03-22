"""Quick Gemini model test."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

models = ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash", "gemini-pro"]
for name in models:
    try:
        model = genai.GenerativeModel(name)
        resp = model.generate_content("Say hi")
        print(f"OK: {name} -> {resp.text[:30]}")
        break
    except Exception as e:
        print(f"FAIL: {name} -> {type(e).__name__}: {e}")
