import requests
import random

class LLMChatClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def start_conversation(self, starter_message, model_name):
        endpoint = f"{self.base_url}/start_conversation"
        data = {
            "starter": starter_message,
            "model_name": model_name
        }
        response = requests.post(endpoint, json=data)
        return response.json()

    def send_message(self, session_id, message, model_name):
        endpoint = f"{self.base_url}/send_message"
        data = {
            "session_id": session_id,
            "message": message,
            "model_name": model_name
        }
        response = requests.post(endpoint, json=data)
        return response.json()

    def generate_message(self, session_id, model_name):
        endpoint = f"{self.base_url}/generate_message"
        data = {
            "session_id": session_id,
            "model_name": model_name
        }
        response = requests.post(endpoint, json=data)
        return response.json()

    def get_session_history(self, session_id):
        endpoint = f"{self.base_url}/session_history/{session_id}"
        response = requests.get(endpoint)
        return response.json()

    def list_models(self):
        endpoint = f"{self.base_url}/models"
        response = requests.get(endpoint)
        return response.json()



def main():
    client = LLMChatClient("http://localhost:8000")

    models = client.list_models()

    print("Available models:", models)

    starter_message = input("Enter the starter message for the conversation: ")
    model_a = random.choice(models)
    start_response = client.start_conversation(starter_message, model_a)
    session_id = start_response['session_id']
    print("Session ID:", session_id)
    print("Model A:", start_response['response'])

    try:
        while True:
            model_b = random.choice(models)
            response_b = client.generate_message(session_id, model_b)
            print("Model B:", response_b['response'])

            model_a = random.choice(models)
            response_a = client.generate_message(session_id, model_a)
            print("Model A:", response_a['response'])

            input()
    except KeyboardInterrupt:
        print("Conversation ended.")

    history = client.get_session_history(session_id)
    print("\nConversation History:")
    for message in history:
        print(f"{message}")


if __name__ == "__main__":
    main()
