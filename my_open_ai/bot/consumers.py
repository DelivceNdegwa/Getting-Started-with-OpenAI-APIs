import json

from channels.generic.websocket import WebsocketConsumer

from .open_ai_script import open_ai_completions_request



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message = text_data_json["message"]
        message = open_ai_completions_request(text_data_json["message"])

        self.send(text_data=json.dumps({"message": message}))