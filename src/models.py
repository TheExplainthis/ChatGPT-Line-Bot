from typing import List, Dict
import requests
import opencc

s2t_converter = opencc.OpenCC('s2t.json')
t2s_converter = opencc.OpenCC('t2s.json')


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
        try:
            r = requests.get('https://api.openai.com/v1/models', headers=self.headers)
            r = r.json()
            if r.get('error'):
                return False, r.get('error', {}).get('message')
        except Exception:
            return False, 'OpenAI API 系統不穩定，請稍後再試'
        return True, None

    def _request(self, endpoint, body):
        try:
            self.headers['Content-Type'] = 'application/json'
            r = requests.post(f'{self.base_url}{endpoint}', headers=self.headers, json=body)
            r = r.json()
            if r.get('error'):
                return False, None, r.get('error', {}).get('message')
        except Exception:
            return False, None, 'OpenAI API 系統不穩定，請稍後再試'
        return True, r, None

    def _request_with_file(self, endpoint, files):
        try:
            self.headers.pop('Content-Type', None)
            r = requests.post(f'{self.base_url}{endpoint}', headers=self.headers, files=files)
            r = r.json()
            if r.get('error'):
                return False, None, r.get('error', {}).get('message')
        except Exception:
            return False, None, 'OpenAI API 系統不穩定，請稍後再試'
        return True, r, None

    def chat_completions(self, messages, model_engine) -> str:
        json_body = {
            'model': model_engine,
            'messages': messages
        }
        is_successful, r, error_message = self._request('/chat/completions', body=json_body)
        if not is_successful:
            return None, None, error_message
        role = r['choices'][0]['message']['role']
        content = r['choices'][0]['message']['content'].strip()
        response = s2t_converter.convert(content)
        return role, response, None

    def audio_transcriptions(self, file_path, model_engine) -> str:
        files = {
            'file': open(file_path, 'rb'),
            'model': (None, 'whisper-1'),
        }
        is_successful, r, error_message = self._request_with_file('/audio/transcriptions', files)
        if not is_successful:
            return None, error_message
        return r['text'], None

    def image_generations(self, prompt: str) -> str:
        json_body = {
            "prompt": prompt,
            "n": 1,
            "size": "512x512"
        }
        is_successful, r, error_message = self._request('/images/generations', json_body)
        if not is_successful:
            return None, error_message
        return r['data'][0]['url'], None
