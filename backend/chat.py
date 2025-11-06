from typing import List, Dict


class Chat:
    def __init__(self, initial_prompt):
        self.initial_prompt = initial_prompt
        self.chat: List[Dict[str, str]] = [{"role": "system",
                                            "content": initial_prompt}]

    def add_user_message(self, text: str):
        self.chat.append({"role": "user", "content": text})

    def add_model_response(self, text: str):
        self.chat.append({"role": "assistant", "content": text})

    def get_chat(self):
        return self.chat

    def new_chat(self):
        self.chat = [{"role": "system", "content": self.initial_prompt}]
