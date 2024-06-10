from pydantic import BaseModel


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


class MessageResponse(BaseModel):
    response: str
    session_id: str
