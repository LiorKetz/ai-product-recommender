from fastapi import FastAPI
from pydantic import BaseModel
from chat import Chat
from model import send_to_model
from fastapi.middleware.cors import CORSMiddleware
from prompts import INITIAL_PROMPT, recommendation_prompt, conversation_summary_prompt
from data_handler import get_products_by_category
import json
import re


app = FastAPI()
chat_instance = Chat(INITIAL_PROMPT)

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # REPLACE WITH FRONTEND URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    text: str


@app.post("/chat")
async def chat(msg: Message):
    chat_instance.add_user_message(msg.text)
    answer = call_model()
    chat_instance.add_model_response(answer)
    return {"response": answer}


@app.post("/new_chat")
async def new_chat():
    chat_instance.new_chat()
    return {"status": "chat reset"}


def parse_json_answer(answer: str):
    """Extract and safely parse JSON from the model's output."""
    # Try to extract valid JSON block from the text
    match = re.search(r"\{.*\}", answer, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in model output: {answer}")
    json_text = match.group(0)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        print("Offending text:", json_text)
        raise


def call_model():
    answer = send_to_model(chat_instance.get_chat())
    print("Model answer:", answer)

    # analyze response:
    try:
        parsed = parse_json_answer(answer)

        text_to_user = parsed["Answer"]
        ready = parsed["ready_to_filter"]
        category = parsed["selected_category"]

        if ready:
            print("Getting product recommendations for category:", category)
            return get_product_recommendations(category)
        else:  # don't have enough info yet, ask for clarification
            return text_to_user
        
    except Exception as e:
        print("Error parsing model response:", e)


def get_chat_summary():
    print("Generating chat summary...")
    chat_history = chat_instance.get_chat()[1:]  # exclude system prompt
    chat_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
    prompt_text = conversation_summary_prompt.format(chat_history=chat_text)

    # call model:
    summary = send_to_model(prompt_text)
    print("Chat summary:", summary)
    return summary


def get_product_recommendations(category):
    # First, get chat summary and extract products
    chat_summary = get_chat_summary()
    products = get_products_by_category(category)
    products = "\n".join([str(p) for p in products])

    # Now, create recommendation prompt
    prompt_text = recommendation_prompt.format(chat_summary=chat_summary, products_str=products)
    print("Recommendation prompt text:", prompt_text)

    # Call model for recommendation
    recommendation = send_to_model(prompt_text)
    print("Product recommendation:", recommendation)
    return recommendation