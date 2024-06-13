from config import load_config
from services.chat import ChatService
from services.history_repo.in_memory_history_repository import InMemoryHistoryRepository
from services.history_repo.on_disk_history_repository import OnDiskHistoryRepository


def get_history_repository(config):
    if config.history_repo.backend == "disk":
        return OnDiskHistoryRepository(config.history_repo.path)
    return InMemoryHistoryRepository()


def get_chat_service(config):
    history_repository = get_history_repository(config)
    return ChatService(config.chat_service, history_repository)


config = load_config()

chat_service = get_chat_service(config)


def get_chat_service():
    return chat_service
