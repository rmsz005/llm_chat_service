import os

from dotenv import load_dotenv

load_dotenv()


def get_config():
    return {
        'models': [
            {
                'model_type': 'gemini',
                'api_key': os.getenv('GOOGLE_API_KEY'),
                'temperature': 0
            },
            # {
            #     'model_type': 'gpt-3.5-turbo',
            #     'api_key': os.getenv('OPENAI_API_KEY'),
            #     'temperature': 0
            # }
        ]
    }
