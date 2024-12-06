from typing_extensions import override
from openai import AssistantEventHandler

class ResponseEventHandler(AssistantEventHandler):
    # This class handles the responses that stream from the open AI API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_text = []

    @override
    def on_text_created(self, text) -> None:
        self.response_text.append(text.value)

    @override
    def on_text_delta(self, delta, snapshot):
        self.response_text.append(delta.value)

    def get_response(self):
        full_response = ''.join(self.response_text)
        return full_response