from fastapi import Depends

from config import get_config
from llm_models.history import ChatSessionManager
from services.chat import ChatService
from services.history_repo.in_memory_history_repository import InMemoryHistoryRepository
from services.history_repo.on_disk_history_repository import OnDiskHistoryRepository


def get_history_repository(config=Depends(get_config)):
    if config.history_repo.backend == "disk":
        return OnDiskHistoryRepository(config.get("storage_path", "./storage"))
    return InMemoryHistoryRepository()


def get_chat_service(history_repository=Depends(get_history_repository)):
    config = get_config()
    session_manager = ChatSessionManager(history_repository)
    return ChatService(config.chat_service, session_manager)
