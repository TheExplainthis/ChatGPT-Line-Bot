from dotenv import load_dotenv
from flask import Flask, request, abort

from linebot.v3 import (WebhookHandler)
from linebot.v3.exceptions import (InvalidSignatureError)
from linebot.v3.messaging import (Configuration, ApiClient, MessagingApi,
                                  ReplyMessageRequest, TextMessage,
                                  ImageMessage, MessagingApiBlob)
from linebot.v3.webhooks import (MessageEvent, TextMessageContent,
                                 AudioMessageContent)


import os
import uuid

from src.models import OpenAIModel
from src.memory import Memory
from src.logger import logger
from src.storage import Storage, FileStorage, MongoStorage
from src.utils import get_role_and_content
from src.service.youtube import Youtube, YoutubeTranscriptReader
from src.service.website import Website, WebsiteReader
from src.mongodb import mongodb

load_dotenv('.env')

app = Flask(__name__)
configuration = Configuration(
    access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

line_bot_api = MessagingApi(ApiClient(configuration))
blob_api = MessagingApiBlob(ApiClient(configuration))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
storage = None
youtube = Youtube(step=4)
website = Website()


memory = Memory(system_message=os.getenv('SYSTEM_MESSAGE'), memory_message_count=2)
model_management = {}
api_keys = {}


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    logger.info(f'{user_id}: {text}')

    try:
        if text.startswith('/註冊'):
            api_key = text[3:].strip()
            model = OpenAIModel(api_key=api_key)
            is_successful, _, _ = model.check_token_valid()
            if not is_successful:
                raise ValueError('Invalid API token')
            model_management[user_id] = model
            storage.save({
                user_id: api_key
                })
            msg = TextMessage(text='Token 有效，註冊成功')

        elif text.startswith('/指令說明'):
            msg = TextMessage(
                text="指令：\n/註冊 + API Token\n👉 API Token 請先到 https://platform.openai.com/ 註冊登入後取得\n\n/系統訊息 + Prompt\n👉 Prompt 可以命令機器人扮演某個角色，例如：請你扮演擅長做總結的人\n\n/清除\n👉 當前每一次都會紀錄最後兩筆歷史紀錄，這個指令能夠清除歷史訊息\n\n/圖像 + Prompt\n👉 會調用 DALL∙E 2 Model，以文字生成圖像\n\n語音輸入\n👉 會調用 Whisper 模型，先將語音轉換成文字，再調用 ChatGPT 以文字回覆\n\n其他文字輸入\n👉 調用 ChatGPT 以文字回覆"
            )

        elif text.startswith('/系統訊息'):
            memory.change_system_message(user_id, text[5:].strip())
            msg = TextMessage(text='輸入成功')

        elif text.startswith('/清除'):
            memory.remove(user_id)
            msg = TextMessage(text='歷史訊息清除成功')

        elif text.startswith('/圖像'):
            prompt = text[3:].strip()
            memory.append(user_id, 'user', prompt)
            is_successful, response, error_message = model_management[user_id].image_generations(prompt)
            if not is_successful:
                raise Exception(error_message)
            url = response['data'][0]['url']
            msg = ImageMessage(original_content_url=url, preview_image_url=url)
            memory.append(user_id, 'assistant', url)

        else:
            user_model = model_management[user_id]
            memory.append(user_id, 'user', text)
            url = website.get_url_from_text(text)
            if url:
                if youtube.retrieve_video_id(text):
                    is_successful, chunks, error_message = youtube.get_transcript_chunks(youtube.retrieve_video_id(text))
                    if not is_successful:
                        raise Exception(error_message)
                    youtube_transcript_reader = YoutubeTranscriptReader(user_model, os.getenv('OPENAI_MODEL_ENGINE'))
                    is_successful, response, error_message = youtube_transcript_reader.summarize(chunks)
                    if not is_successful:
                        raise Exception(error_message)
                    role, response = get_role_and_content(response)
                    msg = TextMessage(text=response)
                else:
                    chunks = website.get_content_from_url(url)
                    if len(chunks) == 0:
                        raise Exception('無法撈取此網站文字')
                    website_reader = WebsiteReader(user_model, os.getenv('OPENAI_MODEL_ENGINE'))
                    is_successful, response, error_message = website_reader.summarize(chunks)
                    if not is_successful:
                        raise Exception(error_message)
                    role, response = get_role_and_content(response)
                    msg = TextMessage(text=response)
            else:
                is_successful, response, error_message = user_model.chat_completions(memory.get(user_id), os.getenv('OPENAI_MODEL_ENGINE'))
                if not is_successful:
                    raise Exception(error_message)
                role, response = get_role_and_content(response)
                msg = TextMessage(text=response)
            memory.append(user_id, role, response)
    except ValueError:
        msg = TextMessage(text='Token 無效，請重新註冊，格式為 /註冊 sk-xxxxx')
    except KeyError:
        msg = TextMessage(text='請先註冊 Token，格式為 /註冊 sk-xxxxx')
    except Exception as e:
        memory.remove(user_id)
        if str(e).startswith('Incorrect API key provided'):
            msg = TextMessage(text='OpenAI API Token 有誤，請重新註冊。')
        elif str(e).startswith('That model is currently overloaded with other requests.'):
            msg = TextMessage(text='已超過負荷，請稍後再試')
        else:
            msg = TextMessage(text=str(e))

    line_bot_api.reply_message_with_http_info(
        ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))


@handler.add(MessageEvent, message=AudioMessageContent)
def handle_audio_message(event: MessageEvent):
    print(event)
    user_id = event.source.user_id

    audio_content = blob_api.get_message_content(event.message.id)

    input_audio_path = f'{str(uuid.uuid4())}.m4a'
    with open(input_audio_path, 'wb') as fd:
        fd.write(audio_content)

    try:
        if not model_management.get(user_id):
            raise ValueError('Invalid API token')
        else:
            is_successful, response, error_message = model_management[
                user_id].audio_transcriptions(input_audio_path, 'whisper-1')
            if not is_successful:
                raise Exception(error_message)
            memory.append(user_id, 'user', response['text'])
            is_successful, response, error_message = model_management[
                user_id].chat_completions(memory.get(user_id), 'gpt-3.5-turbo')
            if not is_successful:
                raise Exception(error_message)
            role, response = get_role_and_content(response)
            memory.append(user_id, role, response)
            msg = TextMessage(text=response)
    except ValueError:
        msg = TextMessage(text='請先註冊你的 API Token，格式為 /註冊 [API TOKEN]')
    except KeyError:
        msg = TextMessage(text='請先註冊 Token，格式為 /註冊 sk-xxxxx')
    except Exception as e:
        memory.remove(user_id)
        if str(e).startswith('Incorrect API key provided'):
            msg = TextMessage(text='OpenAI API Token 有誤，請重新註冊。')
        else:
            msg = TextMessage(text=str(e))
    os.remove(input_audio_path)
    line_bot_api.reply_message_with_http_info(
        ReplyMessageRequest(reply_token=event.reply_token, messages=[msg]))


@app.route("/", methods=['GET'])
def home():
    return 'Hello World'


if __name__ == "__main__":
    if os.getenv('USE_MONGO'):
        mongodb.connect_to_database()
        storage = Storage(MongoStorage(mongodb.db))
    else:
        storage = Storage(FileStorage('db.json'))
    try:
        data = storage.load()
        for user_id in data.keys():
            model_management[user_id] = OpenAIModel(api_key=data[user_id])
    except FileNotFoundError:
        pass
    app.run(host='0.0.0.0', port=8080)
