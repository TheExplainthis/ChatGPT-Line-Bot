from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, AudioMessage
)
import os
import uuid

from src.models import OpenAIModel
from src.memory import Memory
from src.logger import logger
from src.storage import Storage

load_dotenv('.env')

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
storage = Storage('db.json')

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
def handle_text_message(event):
    user_id = event.source.user_id
    text = event.message.text
    logger.info(f'{user_id}: {text}')
    if text.startswith('/註冊'):
        if len(text.split(' ')) == 2:
            _, api_key = text.split(' ')
            model = OpenAIModel(api_key=api_key)
            sucessful = model.check_token_valid()
            if not sucessful:
                msg = TextSendMessage(text='Token 無效，請重新註冊，格式為 /註冊 sk-xxxxx')
            else:
                model_management[user_id] = model
                api_keys[user_id] = api_key
                storage.save(api_keys)
                msg = TextSendMessage(text='Token 有效，註冊成功')
        else:
            msg = TextSendMessage(text='Token 無效，請重新註冊，格式為 /註冊 sk-xxxxx')

    elif text.startswith('/系統訊息'):
        _, system_message = text.split(' ')
        memory.change_system_message(user_id, system_message)
        msg = TextSendMessage(text='輸入成功')

    elif text.startswith('/清除'):
        memory.remove(user_id)
        msg = TextSendMessage(text='歷史訊息清除成功')

    else:
        if not model_management.get(user_id):
            msg = TextSendMessage(text='請先註冊你的 API Token，格式為 /註冊 [API TOKEN]')
        else:
            memory.append(user_id, {
                'role': 'user',
                'content': text
            })
            if text.startswith('/圖像'):
                text = text[3:].strip()
                role = 'assistant'
                response, error_message = model_management[user_id].image_generations(text)
                if error_message:
                    msg = TextSendMessage(text=error_message)
                    memory.remove(user_id)
                else:
                    msg = ImageSendMessage(
                        original_content_url=response,
                        preview_image_url=response
                    )
                    memory.append(user_id, {
                        'role': role,
                        'content': response
                    })
            else:
                role, response, error_message = model_management[user_id].chat_completions(memory.get(user_id), os.getenv('OPENAI_MODEL_ENGINE'))
                if error_message:
                    msg = TextSendMessage(text=error_message)
                    memory.remove(user_id)
                else:
                    msg = TextSendMessage(text=response)
                    memory.append(user_id, {
                        'role': role,
                        'content': response
                    })
    line_bot_api.reply_message(event.reply_token, msg)


@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    user_id = event.source.user_id
    audio_content = line_bot_api.get_message_content(event.message.id)
    input_audio_path = f'{str(uuid.uuid4())}.m4a'
    with open(input_audio_path, 'wb') as fd:
        for chunk in audio_content.iter_content():
            fd.write(chunk)

    transciption, error_message = model_management[user_id].audio_transcriptions(input_audio_path, 'whisper-1')
    if error_message:
        os.remove(input_audio_path)    
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_message))
        return
    memory.append(user_id, {
        'role': 'user',
        'content': transciption
    })

    role, response, error_message = model_management[user_id].chat_completions(memory.get(user_id), 'gpt-3.5-turbo')
    if error_message:
        os.remove(input_audio_path)    
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_message))
        memory.remove(user_id)
        return
    memory.append(user_id, {
        'role': role,
        'content': response
    })
    os.remove(input_audio_path)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))


@app.route("/", methods=['GET'])
def home():
    return 'Hello World'


if __name__ == "__main__":
    try:
        data = storage.load()
        for user_id in data.keys():
            model_management[user_id] = OpenAIModel(api_key=data[user_id])
    except FileNotFoundError:
        pass
    app.run(host='0.0.0.0', port=8080)
