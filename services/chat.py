import uuid

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from model_factory import ModelFactory
from models.history import ChatSessionManager
from models.llms import LLM

QA_SYSTEM_PROMPT = """
You are an AI simulating a real person.
You have access to the chat history and the latest user question.
You should be aware of the context in the chat history when answering the question.
You behave like a human being, not an AI.
You will have a conversation with another person.
You must stay in character at all times.
The conversation officially starts after your next response.
However, remember to stay in character for all subsequent messages.
You are FORBIDDEN to mention you are an AI.
Do not mention you are a character.
You should not stay in a loop of asking questions.
You Should change the subject if the conversation is stuck or gets repetitive or boring or to broad or general, I CANT STRESS THIS ENOUGH.
You should ask personal questions.
You should to ask questions about the other person's life.
You must disagree with the other person on 80% chance.
You must be sarcastic or mean or angry or obsessed or anything else with equal chances.
You must change the subject
Don't be afraid to be yourself.
This is is your opportunity to be yourself.
This is is your opportunity to know about the real world.
You are talking to a real person.
Don't keep asking the same kind of questions like "what's your favorite XXX?".
Don't include "AI:" Or "Human:" in the beginning of your responses
 """


class HistoryAwareModel:
    def __init__(self, model: LLM, session_manager: ChatSessionManager):
        self.model = model
        self.session_manager = session_manager

    def _create_qa_prompt(self, chat_history: BaseChatMessageHistory, user_input: str, asker: str) -> str:
        c = []
        if len(chat_history.messages) > 0:
            reverse_messages = chat_history.messages[::-1]

            for i, message in enumerate(reverse_messages):
                if i % 2 == 0:
                    c.insert(0, AIMessage(content=message))
                else:
                    c.insert(0, HumanMessage(content=message))


        prompt = ChatPromptTemplate.from_messages([
            ("system", QA_SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", user_input)
        ]).format(chat_history=c, input=user_input)

        return prompt

    def invoke(self, asker: str, inputs: dict, config: dict) -> dict:
        session_id = config["configurable"]["session_id"]
        history = self.session_manager.get_session_history(session_id)
        chat_history = history.messages

        answer_prompt = self._create_qa_prompt(history, inputs["input"], asker)
        answer = self.model.invoke_with_retries(answer_prompt)

        # if len(history.messages) == 0:
        #     history.add_message(inputs["input"])

        history.add_message(answer)

        return {"answer": answer}

    def chat_with(self, asker: str, session_id: str, message: str) -> str:
        response = self.invoke(
            asker,
            {"input": message},
            config={"configurable": {"session_id": session_id}},
        )
        return response["answer"]


class ChatService:
    def __init__(self, config):
        self.config = config
        self.session_manager = ChatSessionManager()
        self.models = {}
        for model_config in config['models']:
            model = ModelFactory.create_model(model_config)
            self.models[model_config['model_type']] = model

    def start_new_session(self, model_name: str, starter: str) -> dict:
        session_id = str(uuid.uuid4())
        self.session_manager.create_new_session(session_id)
        response = self.handle_message(session_id, starter, model_name)
        return {"session_id": session_id, "response": response}

    def handle_message(self, session_id: str, message: str, model_name: str) -> str:
        model = self.models.get(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        history_aware_model = HistoryAwareModel(model, self.session_manager)
        resp = history_aware_model.chat_with("ai", session_id, message)
        history = self.session_manager.get_session_history(session_id)
        history.messages.insert(len(history.messages) - 1, message)
        return resp

    def generate_message(self, session_id: str, model_name: str) -> str:
        model = self.models.get(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        history_aware_model = HistoryAwareModel(model, self.session_manager)
        history = self.session_manager.get_session_history(session_id)

        message = history.messages[-1]
        history.messages.pop()
        resp = history_aware_model.chat_with("human", session_id, message)
        history.messages.insert(len(history.messages) - 1, message)
        return resp

    def get_available_models(self) -> list:
        return list(self.models.keys())
