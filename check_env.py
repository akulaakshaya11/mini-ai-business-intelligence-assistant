import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

if key:
    print("SUCCESS: Gemini API key was loaded.")
    print("Key length:", len(key))
else:
    print("ERROR: Gemini API key was not found.")
    print("Check that .env is in the project root.")