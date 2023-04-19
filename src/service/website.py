import os
import re
import requests
from bs4 import BeautifulSoup


WEBSITE_SYSTEM_MESSAGE = "你現在非常擅於做資料的整理、總結、歸納、統整，並能專注於細節、且能提出觀點"
WEBSITE_MESSAGE_FORMAT = """
    針對這個連結的內容：
    \"\"\"
    {}
    \"\"\"

    請關注幾個點：
    1. 他的主題為何？
    2. 他的重點為何？
    3. 他獨特的觀點為何？

    你需要回傳的格式是：
    - 主題： '...'
    - 重點： '...'
    - 獨特觀點： '...'
"""


class Website:
    def get_url_from_text(self, text: str):
        url_regex = re.compile(r'^https?://\S+')
        match = re.search(url_regex, text)
        if match:
            return match.group()
        else:
            return None

    def get_content_from_url(self, url: str):
        hotpage = requests.get(url)
        main = BeautifulSoup(hotpage.text, 'html.parser')
        chunks = [article.text.strip() for article in main.find_all('article')]
        if chunks == []:
            chunks = [article.text.strip() for article in main.find_all('div', class_='content')]
        return chunks


class WebsiteReader:
    def __init__(self, model=None, model_engine=None):
        self.system_message = os.getenv('WEBSITE_SYSTEM_MESSAGE') or WEBSITE_SYSTEM_MESSAGE
        self.message_format = os.getenv('WEBSITE_MESSAGE_FORMAT') or WEBSITE_MESSAGE_FORMAT
        self.model = model
        self.text_length_limit = 1800
        self.model_engine = model_engine

    def send_msg(self, msg):
        return self.model.chat_completions(msg, self.model_engine)

    def summarize(self, chunks):
        text = '\n'.join(chunks)[:self.text_length_limit]
        msgs = [{
            "role": "system", "content": self.system_message
        }, {
            "role": "user", "content": self.message_format.format(text)
        }]
        return self.send_msg(msgs)
