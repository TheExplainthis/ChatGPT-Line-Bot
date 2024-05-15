from typing import List, Dict
import requests


class ModelInterface:
    def check_token_valid(self) -> bool:
        pass

    def list_files(self) -> str:
        pass

    def retrieve_assistant(self) -> str:
        pass

    def retrieve_vector_store(self, vector_store_id: str) -> str:
        pass

    def retrieve_vector_store_files(self, vector_store_id: str) -> str:
        pass

    def create_thread(self) -> str:
        pass

    def retrieve_thread(self) -> str:
        pass

    def delete_thread(self, thread_id: str) -> bool:
        pass

    def create_thread_message(self, thread_id: str, messages: List[Dict]) -> bool:
        pass

    def list_thread_messages(self, thread_id: str) -> str:
        pass

    def create_thread_run(self, thread_id: str) -> str:
        pass

    def retrieve_thread_run(self, thread_id: str, run_id:str) -> str:
        pass

    def chat_completions(self, messages: List[Dict], model_engine: str) -> str:
        pass

    def audio_transcriptions(self, file, model_engine: str) -> str:
        pass

    def image_generations(self, prompt: str) -> str:
        pass


class OpenAIModel(ModelInterface):
    def __init__(self, api_key: str, assistant_id: str):
        self.api_key = api_key
        self.assistant_id = assistant_id
        self.base_url = 'https://api.openai.com/v1'

    def _request(self, method, endpoint, body=None, files=None, assistant=False):
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        try:
            if method == 'GET':
                if assistant:
                    self.headers['Content-Type'] = 'application/json'
                    self.headers['OpenAI-Beta'] = 'assistants=v2'
                r = requests.get(f'{self.base_url}{endpoint}', headers=self.headers)
            elif method == 'POST':
                if body:
                    self.headers['Content-Type'] = 'application/json'
                if assistant:
                    self.headers['OpenAI-Beta'] = 'assistants=v2'
                r = requests.post(f'{self.base_url}{endpoint}', headers=self.headers, json=body, files=files)
            r = r.json()
            if r.get('error'):
                return False, None, r.get('error', {}).get('message')
        except Exception:
            return False, None, 'OpenAI API 系統不穩定，請稍後再試'
        return True, r, None

    def check_token_valid(self) -> bool:
        return self._request('GET', '/models')

    def list_files(self) -> str:
        endpoint = '/files'
        return self._request('GET', endpoint, assistant=True)

    def retrieve_assistant(self) -> str:
        endpoint = '/assistants/' + self.assistant_id
        return self._request('GET', endpoint, assistant=True)

    def retrieve_vector_store(self, vector_store_id) -> str:
        endpoint = '/vector_stores/' + vector_store_id
        return self._request('GET', endpoint, assistant=True)

    def list_vector_store_files(self, vector_store_id) -> str:
        endpoint = '/vector_stores/' + vector_store_id + '/files'
        return self._request('GET', endpoint, assistant=True)

    def create_thread(self) -> str:
        endpoint = '/threads'
        return self._request('POST', endpoint, assistant=True)

    def retrieve_thread(self, thread_id) -> str:
        endpoint = '/threads/' + thread_id
        return self._request('GET', endpoint, assistant=True)

    def delete_thread(self, thread_id) -> bool:
        endpoint = '/threads/' + thread_id
        return self._request('DELETE', endpoint, assistant=True)

    def create_thread_message(self, thread_id, messages) -> bool:
        endpoint = '/threads/' + thread_id + '/messages'
        json_body = {
            'role': 'user',
            'content': messages
        }
        return self._request('POST', endpoint, body=json_body, assistant=True)

    def create_thread_run(self, thread_id) -> str:
        endpoint = '/threads/' + thread_id + '/runs'
        json_body = {
            'assistant_id': self.assistant_id,
            'temperature': 0
        }
        return self._request('POST', endpoint, body=json_body, assistant=True)

    def retrieve_thread_run(self, thread_id, run_id) -> str:
        endpoint = '/threads/' + thread_id + '/runs/' + run_id
        return self._request('GET', endpoint, assistant=True)

    def list_thread_messages(self, thread_id) -> str:
        endpoint = '/threads/' + thread_id + '/messages'
        return self._request('GET', endpoint, assistant=True)

    def chat_completions(self, messages, model_engine) -> str:
        json_body = {
            'model': model_engine,
            'messages': messages
        }
        return self._request('POST', '/chat/completions', body=json_body)

    def audio_transcriptions(self, file_path, model_engine) -> str:
        files = {
            'file': open(file_path, 'rb'),
            'model': (None, model_engine),
        }
        return self._request('POST', '/audio/transcriptions', files=files)

    def image_generations(self, prompt: str) -> str:
        json_body = {
            "prompt": prompt,
            "n": 1,
            "size": "512x512"
        }
        return self._request('POST', '/images/generations', body=json_body)
