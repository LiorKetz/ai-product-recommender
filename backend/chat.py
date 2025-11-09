from typing import List, Dict
from uuid import uuid4
from datetime import datetime

class Chat:
    def __init__(self, initial_prompt):
        self.session_id = str(uuid4())
        self.initial_prompt = initial_prompt
        self.feedback = "none"
        self.timestamp_start = datetime.now().isoformat()
        self.chat: List[Dict[str, str]] = [{"role": "system",
                                            "content": initial_prompt}]
        self.monitoring_log: List[Dict[str, str, float]] = [{"role": "system",
                                            "content": initial_prompt,
                                            "latency_seconds": 0.0}]

    def add_user_message(self, text: str):
        self.chat.append({"role": "user", "content": text})

    def add_model_response(self, text: str):
        self.chat.append({"role": "assistant", "content": text})

    def add_monitoring_log(self, role: str, text: str, latency_seconds: float = 0.0):
        self.monitoring_log.append({"role": role, "content": text, "latency_seconds": latency_seconds})

    def get_chat(self):
        return self.chat

    def get_monitoring_log(self):
        return self.monitoring_log

    def new_chat(self):
        # self.chat = [{"role": "system", "content": self.initial_prompt}]
        self.chat = self.chat[:1]
        self.monitoring_log = self.monitoring_log[:1]

    def set_feedback(self, feedback: str):
        if feedback in ["positive", "negative", "none"]:
            self.feedback = feedback
        else:
            raise ValueError("Feedback must be 'positive', 'negative', or 'none'")
    
    def log_conversation(self):
        # add self.monitoring_log to conversations_log.jsonl
        total_messages = len(self.monitoring_log)
        user_turns = sum(1 for entry in self.monitoring_log if entry['role'] == 'user')
        agent_turns = sum(1 for entry in self.monitoring_log if entry['role'] == 'assistant')

        avg_latency = sum(item["latency_seconds"] for item in self.monitoring_log if "latency_seconds" in item) / agent_turns

        log_entry = {
            "session_id": self.session_id,
            "timestamp_start": self.timestamp_start,
            "timestamp_end": datetime.now().isoformat(),
            "total_messages": total_messages,
            "user_turns": user_turns,
            "agent_turns": agent_turns,
            "user_feedback":  self.feedback,
            "average_latency_seconds": avg_latency,
            "conversation_history": self.monitoring_log,
        }

        return log_entry
