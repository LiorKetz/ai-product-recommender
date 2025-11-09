from typing import List, Dict
from uuid import uuid4
from datetime import datetime

class Chat:
    """
    A class to manage chat sessions, including user messages,
    model responses, monitoring logs, and user feedback.
    
    Attributes:
        session_id (str): Unique identifier for the chat session.
        feedback (str): User feedback for the session ('positive', 'negative', 'none').
        timestamp_start (str): ISO formatted timestamp when the chat started.
        chat (List[Dict[str, str]]): List of messages in the chat.
        monitoring_log (List[Dict[str, str, float]]): List of monitoring log entries.
    """

    def __init__(self, initial_prompt):
        """
        Initialize a new chat session.
        
        Parameters:
            initial_prompt (str): The initial system prompt for the chat.
        Returns:
            None
        """
        self.session_id = str(uuid4())
        self.feedback = "none"
        self.timestamp_start = datetime.now().isoformat()

        self.chat: List[Dict[str, str]] = [{"role": "system",
                                            "content": initial_prompt}]
        self.monitoring_log: List[Dict[str, str, float]] = [{"role": "system",
                                            "content": initial_prompt,
                                            "latency_seconds": 0.0}]

    def add_user_message(self, text: str):
        """
        Add a user message to the chat.

        Parameters:
            text (str): The user's message.
        Returns:
            None
        """
        self.chat.append({"role": "user", "content": text})

    def add_model_response(self, text: str):
        """
        Add a model response to the chat.

        Parameters:
            text (str): The model's response.
        
        Returns:
            None
        """
        self.chat.append({"role": "assistant", "content": text})

    def add_monitoring_log(self, role: str, text: str, latency_seconds: float = 0.0):
        """
        Add an entry to the monitoring log.

        Parameters:
            role (str): The role of the message sender ('user' or 'assistant').
            text (str): The content of the message.
            latency_seconds (float): The latency in seconds for the model response (default is 0.0).
        Returns:
            None
        """
        self.monitoring_log.append({"role": role, "content": text, "latency_seconds": latency_seconds})

    def get_chat(self):
        """
        Get the current chat history.
        
        Returns:
            List[Dict[str, str]]: The chat history.
        """
        return self.chat

    def get_monitoring_log(self):
        """
        Get the current monitoring log.

        Returns:
            List[Dict[str, str, float]]: The monitoring log.
        """
        return self.monitoring_log

    def new_chat(self):
        """
        Start a new chat session, resetting chat history and monitoring log
        while retaining the initial system prompt.
        
        Returns:
            None
        """
        self.chat = self.chat[:1]
        self.monitoring_log = self.monitoring_log[:1]
        self.session_id = str(uuid4())
        self.timestamp_start = datetime.now().isoformat()
        self.feedback = "none"

    def set_feedback(self, feedback: str):
        """
        Set user feedback for the chat session.

        Parameters:
            feedback (str): The user feedback ('positive', 'negative', or 'none').
        Returns:
            None
        """
        if feedback in ["positive", "negative", "none"]:
            self.feedback = feedback
        else:
            raise ValueError("Feedback must be 'positive', 'negative', or 'none'")
    
    def log_conversation(self):
        """
        Create a log entry for the conversation.

        Returns:
            Dict[str, Any]: The log entry for the conversation.
        """
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
