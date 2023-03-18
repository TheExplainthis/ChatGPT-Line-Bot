from typing import List, Dict
import requests


class ModelInterface:
    def check_token_valid(self) -> bool:
        pass

    def chat_completions(self, messages: List[Dict]) -> str:
        pass

    def audio_transcriptions(self, file) -> str:
        pass

    def image_generations(self, prompt: str) -> str:
        pass


class OpenAIModel(ModelInterface):
    def __init__(self, api_key: str):
        self.headers = {
            'Authorization': f'Bearer {api_key}'
        }
        self.base_url = 'https://api.openai.com/v1'

    def check_token_valid(self):
        r = requests.get('https://api.openai.com/v1/models', headers=self.headers)
        if r.json().get('error'):
            return False
        return True

    def _request(self, endpoint, body):
        self.headers['Content-Type'] = 'application/json'
        r = requests.post(f'{self.base_url}{endpoint}', headers=self.headers, json=body)
        return r.json()

    def _request_with_file(self, endpoint, files):
        self.headers.pop('Content-Type', None)
        r = requests.post(f'{self.base_url}{endpoint}', headers=self.headers, files=files)
        return r.json()

    def chat_completions(self, messages, model_engine) -> str:
        json_body = {
            'model': model_engine,
            'messages': messages
        }
        r = self._request('/chat/completions', body=json_body)
        role = r['choices'][0]['message']['role']
        content = r['choices'][0]['message']['content']
        return role, content

    def audio_transcriptions(self, file_path, model_engine) -> str:
        files = {
            'file': open(file_path, 'rb'),
            'model': (None, 'whisper-1'),
        }
        r = self._request_with_file('/audio/transcriptions', files)
        return r['text']

    def image_generations(self, prompt: str) -> str:
        json_body = {
            "prompt": prompt,
            "n": 1,
            "size": "512x512"
        }
        r = self._request('/images/generations', json_body)
        return r['data'][0]['url']
