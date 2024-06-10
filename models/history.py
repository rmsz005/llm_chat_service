from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory


class ChatSessionManager:
    def __init__(self):
        self.store = {}

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        # if session_id not in self.store:
        #     self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def create_new_session(self, session_id: str):
        self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
