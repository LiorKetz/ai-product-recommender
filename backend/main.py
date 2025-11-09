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
from typing import List, Dict, Any


app = FastAPI()

chat_instance = Chat(INITIAL_PROMPT)
LOG_FILE_PATH = Path(__file__).parent / 'db' / 'conversations_log.jsonl'

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # FRONTEND URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    """
    Data model for a chat message.

    Attributes:
        text (str): The content of the message.
    """
    text: str


class FeedbackData(BaseModel):
    """
    Data model for user feedback.

    Attributes:
        feedback (str): The user feedback ('positive', 'negative', or 'none').
    """
    feedback: str  # 'positive' / 'negative' / 'none'


@app.post("/chat")
async def chat(msg: Message):
    """
    Handle a chat message from the user and return the model's response.

    Parameters:
        msg (Message): The user's message.
    Returns:
        Dict[str, Any]: The model's response and recommendation flag.
    """
    chat_instance.add_user_message(msg.text)
    chat_instance.add_monitoring_log(role="user", text=msg.text)
    answer, is_rec = call_model()
    chat_instance.add_model_response(answer)
    return {"response": answer,
            "is_recommendation": is_rec}


@app.post("/new_chat")
async def new_chat():
    """
    Start a new chat session, logging the previous one.
    
    Returns:
        Dict[str, str]: Status message.
    """
    log_conversation()
    chat_instance.new_chat()
    return {"status": "chat reset"}


@app.post("/feedback")
async def feedback(data: FeedbackData):
    """
    Receive user feedback for the chat session.
    
    Parameters:
        data (FeedbackData): The user feedback.
    Returns:
        Dict[str, str]: Status
    """
    chat_instance.set_feedback(data.feedback)
    print(f"Feedback received: {data.feedback}")
    return {"status": "feedback received"}


@app.get("/logs")
async def get_logs():
    """
    Get aggregated logs statistics.

    Returns:
        Dict[str, Any]: Aggregated statistics from the logs.
    """
    logs = read_logs_from_file(LOG_FILE_PATH)
    
    # If no logs, return empty stats
    if not logs:
        return get_empty_stats()
    
    # Calculate statistics
    feedback_count, positive_percent = calculate_feedback_stats(logs)
    
    # Compile final stats
    stats = {
        "total_chats": len(logs),
        "chats_with_feedback": feedback_count,
        "positive_feedback_percent": positive_percent,
        "avg_conversation_duration_sec": calculate_avg_duration(logs),
        "avg_messages_per_chat": calculate_avg_messages(logs),
        "recent_sessions": format_recent_sessions(logs)
    }
    
    return stats


def read_logs_from_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Read and parse log entries from file.

    Parameters:
        file_path (str): Path to the log file.
    Returns:
        List[Dict[str, Any]]: List of log entries.
    """

    logs = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    logs.append(json.loads(line))
    except FileNotFoundError:
        return []
    return logs


def get_empty_stats() -> Dict[str, Any]:
    """
    Return empty statistics structure.
    
    Returns:
        Dict[str, Any]: Empty statistics.
    """

    return {
        "total_chats": 0,
        "chats_with_feedback": 0,
        "positive_feedback_percent": 0,
        "avg_conversation_duration_sec": 0,
        "avg_messages_per_chat": 0,
        "recent_sessions": []
    }


def calculate_feedback_stats(logs: List[Dict[str, Any]]) -> tuple[int, float]:
    """
    Calculate feedback statistics.
    
    Returns:
        tuple: (chats_with_feedback_count, positive_feedback_percent)
    """
    chats_with_feedback = [log for log in logs if log["user_feedback"] != "none"]
    positive_feedback = [log for log in chats_with_feedback if log["user_feedback"] == "positive"]
    
    feedback_count = len(chats_with_feedback)
    positive_percent = round((len(positive_feedback) / feedback_count) * 100, 2) if feedback_count > 0 else 0
    
    return feedback_count, positive_percent


def calculate_avg_duration(logs: List[Dict[str, Any]]) -> float:
    """
    Calculate average conversation duration in seconds.
    
    Returns:
        float: Average duration in seconds.
    """
    total_duration = 0
    valid_durations = 0
    
    for log in logs:
        try:
            start = parse_time(log["timestamp_start"])
            end = parse_time(log["timestamp_end"])
            total_duration += (end - start).total_seconds()
            valid_durations += 1
        except (KeyError, ValueError, TypeError):
            continue
    
    return round(total_duration / valid_durations, 2) if valid_durations > 0 else 0


def calculate_avg_messages(logs: List[Dict[str, Any]]) -> float:
    """
    Calculate average messages per chat.

    Parameters:
        logs (List[Dict[str, Any]]): List of log entries.
    """

    if not logs:
        return 0
    total_messages = sum(log.get("total_messages", 0) for log in logs)
    return round(total_messages / len(logs), 2)


def format_recent_sessions(logs: List[Dict[str, Any]], count: int = 5) -> List[Dict[str, Any]]:
    """
    Format recent sessions for response.

    Parameters:
        logs (List[Dict[str, Any]]): List of log entries.
        count (int): Number of recent sessions to return.
    Returns:
        List[Dict[str, Any]]: Formatted recent sessions.
    """

    return [
        {
            "session_id": log.get("session_id", "unknown"),
            "feedback": log.get("user_feedback"),
            "total_messages": log.get("total_messages", 0),
            "average_latency_seconds": log.get("average_latency_seconds"),
        }
        for log in logs[-count:]
    ]


def parse_time(timestamp_str: str) -> datetime:
    """
    Parse ISO format timestamp string to datetime object
    
    Parameters:
        timestamp_str (str): ISO formatted timestamp string.
    Returns:
        datetime: Parsed datetime object.
    """

    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))


def parse_json_answer(answer: str):
    """
    Extract and safely parse JSON from the model's output.
    
    Parameters:    
        answer (str): The model's output containing JSON.
    Returns:
        dict: Parsed JSON data.
    """

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
    """
    Call the language model with the current chat context and process the response.
    
    Returns:
        tuple: (model_answer (str), is_recommendation (bool))
    """
    start_time = datetime.now()
    answer = send_to_model(chat_instance.get_chat())
    end_time = datetime.now()
    latency_seconds = (end_time - start_time).total_seconds()
    chat_instance.add_monitoring_log(role="assistant", text=answer, latency_seconds=latency_seconds)
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
    """
    Generate a summary of the chat conversation so far use the model.

    Returns:
        str: The chat summary.
    """

    print("Generating chat summary...")
    chat_history = chat_instance.get_chat()[1:]  # exclude system prompt
    chat_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
    prompt_text = conversation_summary_prompt.format(chat_history=chat_text)
    chat_instance.add_monitoring_log(role="system", text=prompt_text)

    # call model:
    start_time = datetime.now()
    summary = send_to_model(prompt_text)
    end_time = datetime.now()
    latency_seconds = (end_time - start_time).total_seconds()
    chat_instance.add_monitoring_log(role="assistant", text=summary, latency_seconds=latency_seconds)
    print("Chat summary:", summary)
    return summary


def get_product_recommendations(category):
    """
    Get product recommendations based on the chat summary and category.

    Parameters:
        category (str): The product category for recommendations.
    Returns:
        tuple: (recommendation (str), True)
    """
    # First, get chat summary and extract products
    chat_summary = get_chat_summary()
    products = get_products_by_category(category)
    products = "\n".join([str(p) for p in products])

    # Now, create recommendation prompt
    prompt_text = recommendation_prompt.format(chat_summary=chat_summary, products_str=products)
    chat_instance.add_monitoring_log(role="system", text=prompt_text)
    print("Recommendation prompt text:", prompt_text)

    # Call model for recommendation
    start_time = datetime.now()
    recommendation = send_to_model(prompt_text)
    end_time = datetime.now()
    latency_seconds = (end_time - start_time).total_seconds()
    chat_instance.add_monitoring_log(role="assistant", text=recommendation, latency_seconds=latency_seconds)
    print("Product recommendation:", recommendation)
    return recommendation, True


def log_conversation():
    """
    Log the current conversation to the log file.
    """
    log_entry = chat_instance.log_conversation()

    try:
        with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
            json_line = json.dumps(log_entry, ensure_ascii=False)
            f.write(json_line + '\n')
        print(f"SUCCESS: Conversation log saved for session {log_entry['session_id']}")
    except IOError as e:
        print(f"ERROR: Could not write to log file {LOG_FILE_PATH}. Error: {e}")
    
