from llm_models.llms import GoogleGemini, OpenAIGPT


class ModelFactory:
    """Factory class to create models from a configuration."""

    @staticmethod
    def create_model(config):

        if config.api_key == "":
            raise ValueError("API key not provided")

        api_key = config.api_key
        temperature = config.temperature

        if config.backend == "gemini":
            return GoogleGemini(api_key=api_key, temperature=temperature)
        elif config.backend in ["gpt-3.5", "gpt-3.5-turbo", "gpt-4o", "gpt-4-turbo"]:
            return OpenAIGPT(api_key=api_key, model_name=config.backend, temperature=temperature)
        else:
            raise ValueError(f"Unknown model type: {config.backend}")
