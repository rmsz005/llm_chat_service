import asyncio
from abc import ABC, abstractmethod

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


class LLM(ABC):
    def __init__(self, temperature=0):
        self.temperature = temperature

    @abstractmethod
    async def invoke(self, prompt, system=None):
        pass

    async def invoke_with_retries(self, answer_prompt, max_retries=3):
        for attempt in range(max_retries):
            answer = await self.invoke(answer_prompt)
            if answer:  # Check if answer is not empty
                return answer
            print(f"Attempt {attempt + 1} failed, retrying...")
        print("All attempts failed.")
        return None  # Return None if all retries failed


class GoogleGemini(LLM):
    def __init__(self, api_key, temperature=0):
        super().__init__(temperature)
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

    async def invoke(self, prompt, system=None):
        response = await asyncio.to_thread(self.llm.invoke, prompt)
        return response.content


class OpenAIGPT(LLM):
    def __init__(self, api_key, model_name="gpt-3.5-turbo", temperature=0):
        super().__init__(temperature)
        self.llm = ChatOpenAI(model=model_name, api_key=api_key, temperature=temperature)

    async def invoke(self, prompt, system=None):
        messages = [("system", system), ("human", prompt)] if system else [("human", prompt)]
        response = await asyncio.to_thread(self.llm.invoke, messages)
        return response.content
