from flask import Flask, request, abort,render_template, jsonify
from linebot import (
    LineBotApi
)
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage
)

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    AudioMessageContent
)


import os
import uuid
import time

from src.models import OpenAIModel
from src.config import load_config
from src.logger import logger
from src.db import Database
from src.utils import get_response_data, get_content_and_reference, replace_file_name, check_token_valid, get_file_dict, detect_none_references

app = Flask(__name__)
config = load_config()
configuration = Configuration(access_token=config['line']['channel_access_token'])
handler = WebhookHandler(config['line']['channel_secret'])
openai_api_key = config['openai']['api_key']
openai_assistant_id = config['openai']['assistant_id']
database = Database(config['db'])
model = OpenAIModel(api_key=openai_api_key, assistant_id=openai_assistant_id)
file_dict = get_file_dict(model)

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

def handle_assistant_message(user_id, text):
    logger.info(f'{user_id}: {text}')
    database.check_connect()
    logger.debug('database check done')
    global file_dict
    try:
        if text.startswith('/reset'):
            thread_id = database.query_thread(user_id)
            if thread_id:
                model.delete_thread(thread_id)
                database.delete_thread(user_id)
                msg = TextMessage(text='Reset The Chatbot.')
            else:
                msg = TextMessage(text='Nothing to reset.')
        elif text.startswith('/'):
            command = input_string[1:].split()[0]
            if command in config['commands']:
                msg = TextMessage(text=config['commands'][command] + "\n\n")
            else:
                msg = TextMessage(text="Command not found.")
        else:
            thread_id = database.query_thread(user_id)
            if thread_id:
                is_successful, response, error_message = model.retrieve_thread(thread_id)
                if not is_successful:
                    database.delete_thread(user_id)
                    thread_id = None
            if not thread_id:
                is_successful, response, error_message = model.create_thread()
                if not is_successful:
                    raise Exception(error_message)
                else:
                    thread_id = response['id']
            logger.debug('thread_id: ' + thread_id)
            database.save_thread(user_id, thread_id)
            is_successful, response, error_message = model.create_thread_message(thread_id, text)
            if not is_successful:
                raise Exception(error_message)
            is_successful, response, error_message = model.create_thread_run(thread_id)
            if not is_successful:
                raise Exception(error_message)
            while response['status'] != 'completed':
                run_id = response['id']
                if response['status'] == 'queued':
                    time.sleep(10)
                else:
                    time.sleep(3)
                is_successful, response, error_message = model.retrieve_thread_run(thread_id, run_id)
                logger.debug(run_id + ': ' + response['status'])
                if not is_successful:
                    raise Exception(error_message)
            logger.debug(response)
            is_successful, response, error_message = model.list_thread_messages(thread_id)
            if not is_successful:
                raise Exception(error_message)
            logger.debug(response)
            response_message = get_content_and_reference(response, file_dict)
            if detect_none_references(response_message):
                file_dict = get_file_dict()
                response_message = get_content_and_reference(response, file_dict)
            logger.debug(response_message)
            msg = TextMessage(text=response_message)
    except Exception as e:
        if str(e).startswith('Incorrect API key provided'):
            msg = TextMessage(text='OpenAI API Token 有誤，請重新註冊。')
        elif str(e).startswith('That model is currently overloaded with other requests.'):
            msg = TextMessage(text='已超過負荷，請稍後再試')
        else:
            msg = TextMessage(text='發生錯誤：' + str(e))
    return msg


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    msg = handle_assistant_message(user_id, text)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[msg]
            )
        )

@handler.add(MessageEvent, message=AudioMessageContent)
def handle_audio_message(event):
    user_id = event.source.user_id
    with ApiClient(configuration) as api_client:
        line_bot_blob_api = MessagingApiBlob(api_client)
        audio_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
        input_audio_path = f'{str(uuid.uuid4())}.m4a'
        with open(input_audio_path, 'wb') as fd:
            fd.write(audio_content)
        try:
            is_successful, response, error_message = model.audio_transcriptions(input_audio_path, 'whisper-1')
            if not is_successful:
                raise Exception(error_message)
            text = response['text']
            msg = handle_assistant_message(user_id, text)
        except Exception as e:
            if str(e).startswith('Incorrect API key provided'):
                msg = TextMessage(text='OpenAI API Token 有誤，請重新註冊。')
            elif str(e).startswith('That model is currently overloaded with other requests.'):
                msg = TextMessage(text='已超過負荷，請稍後再試')
            else:
                msg = TextMessage(text='發生錯誤：' + str(e))
        os.remove(input_audio_path)
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[msg]
            )
        )
    line_bot_api.reply_message(event.reply_token, msg)


@app.route("/", methods=['GET'])
def home():
    return 'Hello World'

@app.route('/chat')
def index():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json['message']
    response_message = ask_api(user_message)
    return jsonify({'message': response_message})

def ask_api(message):
    text_content = handle_assistant_message('test_user', message)
    return text_content.text


if __name__ == "__main__":
    model.check_token_valid()
    app.run(host='0.0.0.0', port=8080, debug=True)
