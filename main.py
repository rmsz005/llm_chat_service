from fastapi import FastAPI
from pydantic import BaseModel

from services.chat import ChatService
from utils.config import get_config

app = FastAPI()


class MessageRequest(BaseModel):
    session_id: str
    message: str
    model_name: str


class GenerateMessageRequest(BaseModel):
    session_id: str
    model_name: str


class NewSessionRequest(BaseModel):
    model_name: str
    starter: str


config = get_config()
chat_service = ChatService(config)


@app.post("/start_conversation")
def start_conversation(request: NewSessionRequest):
    session_data = chat_service.start_new_session(request.model_name, request.starter)
    return session_data


@app.post("/send_message")
def send_message(request: MessageRequest):
    response = chat_service.handle_message(request.session_id, request.message, request.model_name)
    return {"response": response}


@app.post("/generate_message")
def generate_message(request: GenerateMessageRequest):
    response = chat_service.generate_message(request.session_id, request.model_name)
    return {"response": response}


@app.get("/models")
def get_models():
    return chat_service.get_available_models()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
