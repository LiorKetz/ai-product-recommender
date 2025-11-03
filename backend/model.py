import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("Missing GROQ_API_KEY in .env file")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL_NAME = "llama-3.1-8b-instant"

def send_to_model(chat):
    data = {
        "model": MODEL_NAME,
        "messages": chat,
        "temperature": 0.7
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    answer = result["choices"][0]["message"]["content"]
    return answer
