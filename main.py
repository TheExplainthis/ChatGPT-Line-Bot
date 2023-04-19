from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, AudioMessage, JoinEvent
)
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
from src.event_handler import event_handler

load_dotenv('.env')

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
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


@handler.add(MessageEvent, message=TextMessage)
@event_handler
def handle_text_message(reply_token, user_id, text):
    if user_id is None:
        line_bot_api.reply_message(reply_token, text)
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
            msg = TextSendMessage(text='Token 有效，註冊成功')
        
        elif text.startswith('/目前金鑰'):
            if user_id in model_management:
                msg = TextSendMessage(text=f'目前使用 Token {model_management[user_id].api_key}')
            else:
                msg = TextSendMessage(text='尚未註冊')

        elif text.startswith('/指令說明') or text.startswith('/help'):
            msg = TextSendMessage(
                text="指令：\n/註冊 + API Token\n👉 API Token 請先到 https://platform.openai.com/ 註冊登入後取得\n" + \
                     "\n/目前金鑰\n👉 顯示目前註冊的 API Token\n" + \
                     "\n/系統訊息 + Prompt\n👉 Prompt 可以命令機器人扮演某個角色，例如：請你扮演擅長做總結的人\n" + \
                     "\n/目前系統訊息 \n👉 顯示目前機器人扮演的角色\n" + \
                     "\n/清除\n👉 當前每一次都會紀錄最後兩筆歷史紀錄，這個指令能夠清除歷史訊息\n" + \
                     "\n/圖像 + Prompt\n👉 會調用 DALL∙E 2 Model，以文字生成圖像\n" + \
                     "\n語音輸入\n👉 會調用 Whisper 模型，先將語音轉換成文字，再調用 ChatGPT 以文字回覆\n" + \
                     "\n其他文字輸入\n👉 調用 ChatGPT 以文字回覆\n"
                     )
            logger.info(msg)

        elif text.startswith('/系統訊息'):
            memory.change_system_message(user_id, text[5:].strip())
            msg = TextSendMessage(text='輸入成功')
        
        elif text.startswith('/目前系統訊息'):
            system_message = memory.system_messages.get(user_id) or os.getenv('SYSTEM_MESSAGE')
            msg = TextMessage(text=f'目前系統訊息：{system_message}')

        elif text.startswith('/清除'):
            memory.remove(user_id)
            msg = TextSendMessage(text='歷史訊息清除成功')

        elif text.startswith('/圖像'):
            prompt = text[3:].strip()
            memory.append(user_id, 'user', prompt)
            is_successful, response, error_message = model_management[user_id].image_generations(prompt)
            if not is_successful:
                raise Exception(error_message)
            url = response['data'][0]['url']
            msg = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )
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
                    msg = TextSendMessage(text=response)
                else:
                    chunks = website.get_content_from_url(url)
                    if len(chunks) == 0:
                        raise Exception('無法撈取此網站文字')
                    website_reader = WebsiteReader(user_model, os.getenv('OPENAI_MODEL_ENGINE'))
                    is_successful, response, error_message = website_reader.summarize(chunks)
                    if not is_successful:
                        raise Exception(error_message)
                    role, response = get_role_and_content(response)
                    msg = TextSendMessage(text=response)
            else:
                is_successful, response, error_message = user_model.chat_completions(memory.get(user_id), os.getenv('OPENAI_MODEL_ENGINE'))
                if not is_successful:
                    raise Exception(error_message)
                role, response = get_role_and_content(response)
                msg = TextSendMessage(text=response)
            memory.append(user_id, role, response)
    except ValueError:
        msg = TextSendMessage(text='Token 無效，請重新註冊，格式為 /註冊 sk-xxxxx')
    except KeyError:
        msg = TextSendMessage(text='請先註冊 Token，格式為 /註冊 sk-xxxxx')
    except Exception as e:
        memory.remove(user_id)
        if str(e).startswith('Incorrect API key provided'):
            msg = TextSendMessage(text='OpenAI API Token 有誤，請重新註冊。')
        elif str(e).startswith('That model is currently overloaded with other requests.'):
            msg = TextSendMessage(text='已超過負荷，請稍後再試')
        else:
            msg = TextSendMessage(text=str(e))
    line_bot_api.reply_message(reply_token, msg)


@handler.add(MessageEvent, message=AudioMessage)
@event_handler
def handle_audio_message(reply_token, user_id, message_id):
    if user_id is None:
        line_bot_api.reply_message(reply_token, message_id)
    audio_content = line_bot_api.get_message_content(message_id)
    input_audio_path = f'{str(uuid.uuid4())}.m4a'
    with open(input_audio_path, 'wb') as fd:
        for chunk in audio_content.iter_content():
            fd.write(chunk)

    try:
        if not model_management.get(user_id):
            raise ValueError('Invalid API token')
        else:
            is_successful, response, error_message = model_management[user_id].audio_transcriptions(input_audio_path, 'whisper-1')
            if not is_successful:
                raise Exception(error_message)
            memory.append(user_id, 'user', response['text'])
            is_successful, response, error_message = model_management[user_id].chat_completions(memory.get(user_id), 'gpt-3.5-turbo')
            if not is_successful:
                raise Exception(error_message)
            role, response = get_role_and_content(response)
            memory.append(user_id, role, response)
            msg = TextSendMessage(text=response)
    except ValueError:
        msg = TextSendMessage(text='請先註冊你的 API Token，格式為 /註冊 [API TOKEN]')
    except KeyError:
        msg = TextSendMessage(text='請先註冊 Token，格式為 /註冊 sk-xxxxx')
    except Exception as e:
        memory.remove(user_id)
        if str(e).startswith('Incorrect API key provided'):
            msg = TextSendMessage(text='OpenAI API Token 有誤，請重新註冊。')
        else:
            msg = TextSendMessage(text=str(e))
    os.remove(input_audio_path)
    line_bot_api.reply_message(reply_token, msg)


@handler.add(JoinEvent)
@event_handler
def handle_join_event(reply_token):
    text = '歡迎使用，請輸入 \n/註冊 [OpenAI API key]，來註冊你的 API key\n或輸入 /help 來查看其他指令\n' + \
    '\n注意！如果群組有其他人，會共用同一個 OpenAI key，意味著所有在此群組的發言都會產生費用，此費用為註冊金鑰者需要支付！'
    msg = TextSendMessage(text=text)
    line_bot_api.reply_message(reply_token, msg)


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
