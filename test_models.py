import os
import dotenv
from google import genai

dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print("API Key:", api_key[:10] + "..." if api_key else None)

client = genai.Client(api_key=api_key)
try:
    for model in client.models.list():
        print(model.name, model.supported_actions)
except Exception as e:
    print("Error:", e)
