from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi

from dependencies import get_chat_service
from domain.models import NewSessionRequest, MessageResponse, MessageRequest, GenerateMessageRequest

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="llm_chat api",
        version="1.0.0",
        description="This is a very cool project 420!",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.post("/start_conversation")
async def start_conversation(request: NewSessionRequest, chat_service=Depends(get_chat_service)) -> MessageResponse:
    """
    Starts a new conversation session.
    """
    session_data = await chat_service.start_new_session(request.model_name, request.starter)
    return MessageResponse(**session_data)


@app.post("/send_message")
async def send_message(request: MessageRequest, chat_service=Depends(get_chat_service)) -> MessageResponse:
    """
    Sends a message in an existing conversation session.
    """
    response = await chat_service.handle_message(request.session_id, request.message, request.model_name)
    return MessageResponse(response=response, session_id=request.session_id)


@app.post("/generate_message")
async def generate_message(request: GenerateMessageRequest, chat_service=Depends(get_chat_service)) -> MessageResponse:
    """
    Generates a message in an existing conversation session.
    """
    response = await chat_service.generate_message(request.session_id, request.model_name)
    return MessageResponse(response=response, session_id=request.session_id)


@app.get("/models")
def get_models(chat_service=Depends(get_chat_service)):
    """
    Retrieves a list of available models.
    """
    return chat_service.get_available_models()


@app.get("/session_history/{session_id}")
def get_session_history(session_id: str, chat_service=Depends(get_chat_service)):
    """
    Retrieves the history of a specific conversation session.
    """
    return chat_service.get_session_history(session_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
