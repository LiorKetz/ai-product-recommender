from typing import List, Dict
from uuid import uuid4

class Chat:
    def __init__(self, initial_prompt):
        self.session_id = str(uuid4())
        self.initial_prompt = initial_prompt
        self.chat: List[Dict[str, str]] = [{"role": "system",
                                            "content": initial_prompt}]
        self.monitoring_log: List[Dict[str, str]] = [{"role": "system",
                                            "content": initial_prompt}]

    def add_user_message(self, text: str):
        self.chat.append({"role": "user", "content": text})

    def add_model_response(self, text: str):
        self.chat.append({"role": "assistant", "content": text})

    def add_monitoring_log(self, role: str, text: str):
        self.monitoring_log.append({"role": role, "content": text})

    def get_chat(self):
        return self.chat

    def get_monitoring_log(self):
        return self.monitoring_log

    def new_chat(self):
        # self.chat = [{"role": "system", "content": self.initial_prompt}]
        self.chat = self.chat[:1]
        self.monitoring_log = self.monitoring_log[:1]
