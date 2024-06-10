import uuid

from domain.models import MessageResponse
from llm_models.HistoryawareModel import HistoryAwareModel
from llm_models.history import ChatSessionManager
from utils.model_factory import ModelFactory


class ChatService:
    def __init__(self, config, session_manager: ChatSessionManager):
        self.config = config
        self.session_manager = session_manager
        self.models = {}
        for model_config in config['models']:
            model = ModelFactory.create_model(model_config)
            self.models[model_config['model_type']] = model

    async def start_new_session(self, model_name: str, starter: str) -> dict:
        session_id = str(uuid.uuid4())
        self.session_manager.create_new_session(session_id)
        response = await self.handle_message(session_id, starter, model_name)
        return {"session_id": session_id, "response": response}

    async def handle_message(self, session_id: str, message: str, model_name: str) -> str:
        model = self.models.get(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        history_aware_model = HistoryAwareModel(model, self.session_manager)
        res = await history_aware_model.invoke(session_id, message)
        self.session_manager.add_message_to_history(session_id, message)
        self.session_manager.add_message_to_history(session_id, res)

        return res

    async def generate_message(self, session_id: str, model_name: str) -> str:
        model = self.models.get(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        history_aware_model = HistoryAwareModel(model, self.session_manager)
        response = await history_aware_model.self_invoke(session_id)
        return response

    def get_available_models(self) -> list:
        return list(self.models.keys())

    def get_session_history(self, session_id: str):
        return self.session_manager.get_session_history(session_id).messages
