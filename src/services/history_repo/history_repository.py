from abc import ABC, abstractmethod

from langchain_core.chat_history import BaseChatMessageHistory


class HistoryRepository(ABC):
    @abstractmethod
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        pass

    @abstractmethod
    def create_new_session(self, session_id: str):
        pass

    @abstractmethod
    def add_message(self, session_id: str, message):
        pass
