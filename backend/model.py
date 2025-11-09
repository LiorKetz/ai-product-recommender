import os
import requests
from dotenv import load_dotenv


load_dotenv()

# Load API key from environment variables
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("Missing GROQ_API_KEY in .env file")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Model configuration:
MODEL_NAME = "llama-3.3-70b-versatile"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def send_to_model(input_data):
    """
    Send input data to the Groq model and get the response.

    Parameters:
        input_data (str or List[Dict]): The input prompt as a string or list of messages.
    Returns:
        str: The model's response content.
    """
    # if input is a string, convert to messages format
    if isinstance(input_data, str):
        messages = [{"role": "system", "content": input_data}]
    elif isinstance(input_data, list):
        messages = input_data
    else:
        raise ValueError("input_data must be string or list of messages")

    data = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(API_URL, json=data, headers=HEADERS)
    response.raise_for_status()
    result = response.json()

    answer = result["choices"][0]["message"]["content"]
    print("RAW MODEL ANSWER >>>", answer)
    return answer

