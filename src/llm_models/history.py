from langchain_core.chat_history import BaseChatMessageHistory


class ChatSessionManager:
    def __init__(self, history_repository):
        self.history_repository = history_repository

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        return self.history_repository.get_session_history(session_id)

    def create_new_session(self, session_id: str):
        self.history_repository.create_new_session(session_id)

    def add_message_to_history(self, session_id: str, message):
        self.history_repository.add_message(session_id, message)
