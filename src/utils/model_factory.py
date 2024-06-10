from llm_models.llms import GoogleGemini, OpenAIGPT


class ModelFactory:
    """Factory class to create models from a configuration."""

    @staticmethod
    def create_model(config):
        model_type = config.get("model_type")
        api_key = config.get("api_key")
        temperature = config.get("temperature", 0)

        if model_type == "gemini":
            return GoogleGemini(api_key=api_key, temperature=temperature)
        elif model_type in ["gpt-3.5-turbo", "gpt-4o", "gpt-4-turbo"]:
            return OpenAIGPT(api_key=api_key, model_name=model_type, temperature=temperature)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
