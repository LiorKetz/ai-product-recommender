from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os
from chat import Chat
from model import send_to_model
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
chat_instance = Chat()

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
    answer = send_to_model(chat_instance.get_chat())
    chat_instance.add_model_response(answer)
    return {"response": answer}


@app.post("/new_chat")
async def new_chat():
    chat_instance.new_chat()
    return {"status": "chat reset"}

