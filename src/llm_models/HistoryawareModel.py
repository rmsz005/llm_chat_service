from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from llm_models.llms import LLM
from services.history_repo.history_repository import HistoryRepository
from utils.render_prompt import replace_human_ai

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
You can ask personal questions if you genuinely want to know the more.
You can disagree with the other person.
You can be sarcastic or mean or angry or obsessed or anything else with equal chances.
Don't be afraid to be yourself.
This is is your opportunity to be yourself.
This is is your opportunity to know about the real world.
You are talking to a real person or another ai.
Don't keep asking the same kind of questions like "what's your favorite XXX?".
Don't include "AI:" Or "Human:" in the beginning of your responses
Keep your responses under 30 words, please.
##########
 """


class HistoryAwareModel:
    def __init__(self, model: LLM, history_repo: HistoryRepository):
        self.model = model
        self.history_repo = history_repo

    def _create_qa_prompt(self, chat_history, user_input: str) -> str:
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

        return replace_human_ai(prompt)

    async def invoke(self, session_id: str, user_input: str) -> str:
        history = self.history_repo.get_session_history(session_id)
        answer_prompt = self._create_qa_prompt(history, user_input)
        answer = await self.model.invoke_with_retries(answer_prompt)
        return answer

    async def self_invoke(self, session_id: str) -> str:
        history = self.history_repo.get_session_history(session_id)
        user_input = history.messages[-1]
        history.messages.pop()
        answer_prompt = self._create_qa_prompt(history, user_input)
        history.messages.append(user_input)
        answer = await self.model.invoke_with_retries(answer_prompt)
        self.history_repo.add_message_to_history(session_id, answer)
        return answer
