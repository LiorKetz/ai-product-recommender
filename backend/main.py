from fastapi import FastAPI
from pydantic import BaseModel
from chat import Chat
from model import send_to_model
from fastapi.middleware.cors import CORSMiddleware
from prompts import INITIAL_PROMPT, recommendation_prompt, conversation_summary_prompt
from data_handler import get_products_by_category
import json
import re
from datetime import datetime
from pathlib import Path


app = FastAPI()
chat_instance = Chat(INITIAL_PROMPT)
LOG_FILE_PATH = Path(__file__).parent / 'db' / 'conversations_log.jsonl'

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
    chat_instance.add_monitoring_log(role="user", text=msg.text)
    answer, is_rec = call_model()
    chat_instance.add_model_response(answer)
    return {"response": answer}
            # "is_recommendation": is_rec}


@app.post("/new_chat")
async def new_chat():
    log_conversation()
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
    chat_instance.add_monitoring_log(role="assistant", text=answer)
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
            return text_to_user, False
        
    except Exception as e:
        print("Error parsing model response:", e)


def get_chat_summary():
    print("Generating chat summary...")
    chat_history = chat_instance.get_chat()[1:]  # exclude system prompt
    chat_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
    prompt_text = conversation_summary_prompt.format(chat_history=chat_text)
    chat_instance.add_monitoring_log(role="system", text=prompt_text)

    # call model:
    summary = send_to_model(prompt_text)
    chat_instance.add_monitoring_log(role="assistant", text=summary)
    print("Chat summary:", summary)
    return summary


def get_product_recommendations(category):
    # First, get chat summary and extract products
    chat_summary = get_chat_summary()
    products = get_products_by_category(category)
    products = "\n".join([str(p) for p in products])

    # Now, create recommendation prompt
    prompt_text = recommendation_prompt.format(chat_summary=chat_summary, products_str=products)
    chat_instance.add_monitoring_log(role="system", text=prompt_text)
    print("Recommendation prompt text:", prompt_text)

    # Call model for recommendation
    recommendation = send_to_model(prompt_text)
    chat_instance.add_monitoring_log(role="assistant", text=recommendation)
    print("Product recommendation:", recommendation)
    return recommendation, True


def log_conversation():
    # add chat_instance.monitoring_log to conversations_log.jsonl
    session_id = chat_instance.session_id
    conversation_history = chat_instance.monitoring_log
    timestamp_end = datetime.now().isoformat()
    total_messages = len(conversation_history)
    user_turns = sum(1 for entry in conversation_history if entry['role'] == 'user')
    agent_turns = sum(1 for entry in conversation_history if entry['role'] == 'assistant')

    log_entry = {
        "session_id": session_id,
        "timestamp_end": timestamp_end,
        "total_messages": total_messages,
        "user_turns": user_turns,
        "agent_turns": agent_turns,
        "conversation_history": conversation_history,
        # "user_feedback": "N/A" 
    }

    try:
        with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
            json_line = json.dumps(log_entry, ensure_ascii=False)
            f.write(json_line + '\n')
        print(f"SUCCESS: Conversation log saved for session {session_id}")
    except IOError as e:
        print(f"ERROR: Could not write to log file {LOG_FILE_PATH}. Error: {e}")
    
