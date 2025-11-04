from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os
from chat import Chat
from model import send_to_model


app = FastAPI()
chat_instance = Chat()


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

# Serve a simple HTML page for testing
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
app.mount("/static", StaticFiles(directory="../tests"), name="static")
@app.get("/")
def get_chat_page():
    return FileResponse("../tests/testFrontHTML.html")
