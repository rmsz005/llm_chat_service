import uuid

from domain.models import MessageResponse
from llm_models.HistoryawareModel import HistoryAwareModel
from services.history_repo.history_repository import HistoryRepository
from utils.model_factory import ModelFactory


class ChatService:
    def __init__(self, config, history_repo: HistoryRepository):
        self.config = config
        self.history_repo = history_repo
        self.models = {}
        for model_config in config.models:
            model = ModelFactory.create_model(model_config)
            self.models[model_config.backend] = model

    async def start_new_session(self, model_name: str, starter: str) -> dict:
        session_id = str(uuid.uuid4())
        self.history_repo.create_new_session(session_id)
        response = await self.handle_message(session_id, starter, model_name)
        return {"session_id": session_id, "response": response}

    async def handle_message(self, session_id: str, message: str, model_name: str) -> str:
        model = self.models.get(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        history_aware_model = HistoryAwareModel(model, self.history_repo)
        res = await history_aware_model.invoke(session_id, message)
        self.history_repo.add_message(session_id, message)
        self.history_repo.add_message(session_id, res)

        return res

    async def generate_message(self, session_id: str, model_name: str) -> str:
        model = self.models.get(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        history_aware_model = HistoryAwareModel(model, self.history_repo)
        response = await history_aware_model.self_invoke(session_id)
        return response

    def get_available_models(self) -> list:
        return list(self.models.keys())

    def get_session_history(self, session_id: str):
        return self.history_repo.get_session_history(session_id).messages
