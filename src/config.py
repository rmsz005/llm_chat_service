import os
import yaml
from pydantic import BaseModel, Field
from pydantic.env_settings import BaseSettings


class HistoryRepoConfig(BaseModel):
    backend: str = Field(..., env='HISTORY_REPO_BACKEND')


class LLMModelConfig(BaseModel):
    backend: str
    temperature: float
    api_key: str


class ChatServiceConfig(BaseModel):
    models: list[LLMModelConfig]


class LLMChatConfig(BaseModel):
    history_repo: HistoryRepoConfig
    chat_service: ChatServiceConfig


class Config(BaseSettings):
    llm_chat: LLMChatConfig

    class Config:
        env_prefix = ''  # No prefix for environment variables
        case_sensitive = False


def get_config():
    # Get the config file path from an environment variable
    config_path = os.getenv('CONFIG_FILE_PATH', 'config/config.yml')

    # Load the YAML configuration file
    with open(config_path, 'r') as file:
        config_data = yaml.safe_load(file)

    # Convert the loaded config data into the Config model
    config = Config(**config_data)

    # Override model-specific values from environment variables
    for model in config.llm_chat.chat_service.models:
        model_name = model.backend.upper()
        model.backend = os.getenv(f'LLM_MODEL_{model_name}_BACKEND', model.backend)
        model.temperature = float(os.getenv(f'LLM_MODEL_{model_name}_TEMPERATURE', model.temperature))
        model.api_key = os.getenv(f'LLM_MODEL_{model_name}_API_KEY', model.api_key)

    return config.llm_chat

# Example usage
config = get_config()
print(config)
