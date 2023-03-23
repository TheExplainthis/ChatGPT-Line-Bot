import math
import os
import re
from src.utils import get_role_and_content

from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled


YOUTUBE_SYSTEM_MESSAGE = "你現在非常擅於做資料的整理、總結、歸納、統整，並能專注於細節、且能提出觀點"
PART_MESSAGE_FORMAT = """ PART {} START
下面是一個 Youtube 影片的部分字幕： \"\"\"{}\"\"\" \n\n請總結出這部影片的重點與一些細節，字數約 100 字左右
PART {} END
"""
WHOLE_MESSAGE_FORMAT = "下面是每一個部分的小結論：\"\"\"{}\"\"\" \n\n 請給我全部小結論的總結，字數約 100 字左右"
SINGLE_MESSAGE_FORMAT = "下面是一個 Youtube 影片的字幕： \"\"\"{}\"\"\" \n\n請總結出這部影片的重點與一些細節，字數約 100 字左右"


class Youtube:
    def __init__(self, step):
        self.step = step
        self.chunk_size = 150

    def get_transcript_chunks(self, video_id):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-TW', 'zh', 'ja', 'zh-Hant', 'zh-Hans', 'en', 'ko'])
            text = [t.get('text') for i, t in enumerate(transcript) if i % self.step == 0]
            chunks = ['\n'.join(text[i*self.chunk_size: (i+1)*self.chunk_size]) for i in range(math.ceil(len(text) / self.chunk_size))]
        except NoTranscriptFound:
            return False, [], '目前只支援：中文、英文、日文、韓文'
        except TranscriptsDisabled:
            return False, [], '本影片無開啟字幕功能'
        except Exception as e:
            return False, [], str(e)
        return True, chunks, None

    def retrieve_video_id(self, url):
        regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(regex, url)
        if match:
            return match.group(1)
        else:
            return None


class YoutubeTranscriptReader:
    def __init__(self, model=None, model_engine=None):
        self.summary_system_prompt = os.getenv('YOUTUBE_SYSTEM_MESSAGE') or YOUTUBE_SYSTEM_MESSAGE
        self.part_message_format = os.getenv('PART_MESSAGE_FORMAT') or PART_MESSAGE_FORMAT
        self.whole_message_format = os.getenv('WHOLE_MESSAGE_FORMAT') or WHOLE_MESSAGE_FORMAT
        self.single_message_format = os.getenv('SINGLE_MESSAGE_FORMAT') or SINGLE_MESSAGE_FORMAT
        self.model = model
        self.model_engine = model_engine

    def send_msg(self, msg):
        return self.model.chat_completions(msg, self.model_engine)

    def summarize(self, chunks):
        summary_msg = []
        if len(chunks) > 1:
            for i, chunk in enumerate(chunks):
                msgs = [{
                    "role": "system", "content": self.summary_system_prompt
                }, {
                    "role": "user", "content": self.part_message_format.format(i, chunk, i)
                }]
                _, response, _ = self.send_msg(msgs)
                _, content = get_role_and_content(response)
                summary_msg.append(content)
            text = '\n'.join(summary_msg)
            msgs = [{
                'role': 'system', 'content': self.summary_system_prompt
            }, {
                'role': 'user', 'content': self.whole_message_format.format(text)
            }]
        else:
            text = chunks[0]
            msgs = [{
                'role': 'system', 'content': self.summary_system_prompt
            }, {
                'role': 'user', 'content': self.single_message_format.format(text)
            }]
        return self.send_msg(msgs)
