from langchain_community.chat_message_histories import ChatMessageHistory

from services.history_repo.history_repository import HistoryRepository


class InMemoryHistoryRepository(HistoryRepository):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.store = {}
        return cls._instance

    def get_session_history(self, session_id: str) -> ChatMessageHistory:
        return self.store.get(session_id, ChatMessageHistory())

    def create_new_session(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()

    def add_message(self, session_id: str, message):
        if session_id in self.store:
            self.store[session_id].add_message(message)
        else:
            self.create_new_session(session_id)
            self.add_message(session_id, message)
