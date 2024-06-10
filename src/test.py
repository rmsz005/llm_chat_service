import http.client
import json


class GeminiClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = self.create_connection()
        self.headers = {'Content-Type': 'application/json'}
        self.session_id = None

    def create_connection(self):
        return http.client.HTTPConnection(self.host, self.port)

    def make_post_request(self, endpoint, payload):
        try:
            self.conn.request("POST", endpoint, payload, self.headers)
            res = self.conn.getresponse()
            data = res.read()
            return json.loads(data.decode('utf-8'))
        except (http.client.HTTPException, BrokenPipeError):
            self.conn = self.create_connection()  # Re-establish connection
            self.conn.request("POST", endpoint, payload, self.headers)
            res = self.conn.getresponse()
            data = res.read()
            return json.loads(data.decode('utf-8'))

    def start_conversation(self, model_name, starter):
        payload = json.dumps({
            "model_name": model_name,
            "starter": starter
        })
        response = self.make_post_request("/start_conversation", payload)
        self.session_id = response['session_id']
        return response['response']

    def generate_message(self, model_name):
        if not self.session_id:
            raise ValueError("No session ID found. Please start a conversation first.")

        payload = json.dumps({
            "session_id": self.session_id,
            "model_name": model_name
        })
        response = self.make_post_request("/generate_message", payload)
        return response['response']


if __name__ == "__main__":
    client = GeminiClient("localhost", 8000)

    # Start conversation
    start_response = client.start_conversation("gemini", "Hello, how are you?")
    print("Gemini1: Hello, how are you?")
    print("Gemini2:", start_response)

    i = 1
    try:
        while True:
            # Generate message for the ongoing conversation
            generate_response = client.generate_message("gemini")
            print(f"Gemini{i}: {generate_response}")
            i = i % 2 + 1
            input()

    except KeyboardInterrupt:
        print("Conversation ended.")
