import os
import pickle

from langchain_community.chat_message_histories import ChatMessageHistory

from services.history_repo.history_repository import HistoryRepository


class OnDiskHistoryRepository(HistoryRepository):
    def __init__(self, storage_path: str = "/tmp/chat_history"):
        self.storage_path = storage_path
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

    def _get_session_file(self, session_id: str) -> str:
        return os.path.join(self.storage_path, f"{session_id}.pkl")

    def get_session_history(self, session_id: str) -> ChatMessageHistory:
        session_file = self._get_session_file(session_id)
        if os.path.exists(session_file):
            with open(session_file, 'rb') as file:
                return pickle.load(file)
        return ChatMessageHistory()

    def create_new_session(self, session_id: str):
        session_file = self._get_session_file(session_id)
        with open(session_file, 'wb') as file:
            pickle.dump(ChatMessageHistory(), file)

    def add_message(self, session_id: str, message):
        session_history = self.get_session_history(session_id)
        session_history.add_message(message)
        session_file = self._get_session_file(session_id)
        with open(session_file, 'wb') as file:
            pickle.dump(session_history, file)
