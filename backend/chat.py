from typing import List, Dict

SYSTEM_PROMPT = "You are a helpful assistant."


class Chat:
    def __init__(self):
        self.chat: List[Dict[str, str]] = [{"role": "system",
                                            "content": SYSTEM_PROMPT}]
        
    def add_user_message(self, text: str):
        self.chat.append({"role": "user", "content": text})
    
    def add_model_response(self, text: str):
        self.chat.append({"role": "assistant", "content": text})

    def get_chat(self):
        return self.chat
    
    def new_chat(self):
        self.chat = [{"role": "system", "content": SYSTEM_PROMPT}]
