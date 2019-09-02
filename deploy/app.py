# coding:utf-8
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import random, os, tempfile, errno
from speech_to_text import speech_to_text
from env_var import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, STR_CURRENT_STATUS_RESPOND, \
                    STR_CURRENT_STATUS, STR_ACTIVATE_BOT, STR_DEACTIVATE_BOT, \
                    STR_ACTIVATE_BOT_RESPOND, STR_DUPLICATE_ACTIVATE_BOT_RESPOND, \
                    STR_DEACTIVATE_BOT_RESPOND, STR_DUPLICATE_DEACTIVATE_BOT_RESPOND
#from customer_template import create_customer_template
#from testapiai import send_text_to_dialogflow


# function for create tmp dir for download content
TEMP_PATH = os.path.join(os.path.dirname(__file__), 'tmp')


def make_dir(folder_path):
    if os.path.exists(folder_path) is not True:
        try:
            os.makedirs(folder_path)
        except Exception as err:
            print('[Error]Create folder failed: ', str(err))

def remove_dir(folder_path):
    try:
        os.rmdir(folder_path)
    except Exception as err:
        print('[Error]Delete folder failed: ', str(err))

def check_temp_folder(event):
    source_type = event.source.type
    if source_type == 'group':
        group_id = event.source.group_id
        temp_folder_path = os.path.join(TEMP_PATH, str(group_id))
    elif source_type == 'user': 
        user_id = event.source.user_id
        temp_folder_path = os.path.join(TEMP_PATH, str(user_id))
    else:
        print('[Error]Unknown source type:', source_type)

    return os.path.exists(temp_folder_path), temp_folder_path

def translate_audio(event):
    _, temp_folder_path = check_temp_folder(event)
    # download audio file 
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=temp_folder_path, suffix='.m4a', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
    
    # speech to text 
    recognize_text = speech_to_text(tf.name)
    print('偵測到語音訊息內容: ', recognize_text)
    return recognize_text

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    
    # print packet info
    print('='*40)
    print(body)
    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


 # handle a event which receive a text msg
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
 
    # get message content
    msg = event.message.text
    source_type = event.source.type

    print('【receive type】', source_type)
    print('【text content】', msg) 

    if msg == STR_ACTIVATE_BOT: 
        # create temp directory
        check_folder_result, temp_folder_path = check_temp_folder(event)
        if check_folder_result is not True:
            respond_str = STR_ACTIVATE_BOT_RESPOND
            make_dir(temp_folder_path)
        else:
            respond_str = STR_DUPLICATE_ACTIVATE_BOT_RESPOND

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = respond_str))
    elif msg == STR_DEACTIVATE_BOT:
        # remove temp directory
        check_folder_result, temp_folder_path = check_temp_folder(event)
        if check_folder_result is True:
            respond_str = STR_DEACTIVATE_BOT_RESPOND
            remove_dir(temp_folder_path)
        else:
            respond_str = STR_DUPLICATE_DEACTIVATE_BOT_RESPOND

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = respond_str))
    elif msg == STR_CURRENT_STATUS:
        check_folder_result, temp_folder_path = check_temp_folder(event)
        current_status = 'On' if check_folder_result is True else 'Off'
        respond_str = STR_CURRENT_STATUS_RESPOND.format(current_status=current_status)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = respond_str))


 # handle a event which receive a audio msg
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    source_type = event.source.type
    user_id = event.source.user_id
    print('【receive type】', source_type)

    # do only when translation mode is open
    check_folder_result, _ = check_temp_folder(event)
    if check_folder_result is not True:
        return

    if source_type == 'group':
        group_id = event.source.group_id
        # get speaker frofile
        profile = line_bot_api.get_group_member_profile(group_id, user_id)
        # print(profile.display_name)
        # print(profile.user_id)
        # print(profile.picture_url)

        recognize_text = translate_audio(event)
        if recognize_text == '無法辨識內容':
            reponse_text = '【' + profile.display_name + '】說的話實在是無法翻譯呢...' 
        else:
            reponse_text = '【' + profile.display_name + '】說：\r' + recognize_text
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reponse_text)) 
    elif source_type == 'user':
        recognize_text = translate_audio(event)
        print('偵測到語音訊息內容: ', recognize_text)
        if recognize_text == '無法辨識內容':
            reponse_text = '您說的話實在是無法翻譯呢...'         
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=recognize_text))  
    else:
        print('[Error]Unknown source type:', source_type)
        return


 # handle a event which receive a sticker
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print('【receive type】', event.message.type)
    check_folder_result, _ = check_temp_folder(event)
    if check_folder_result is not True:
        return

    # random choose a sticker to send
    sid = random.randint(1,10)
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=1,
            sticker_id=sid
        )
    )    
 

#  # handle a event which receive others msg
# @handler.add(MessageEvent, message=(LocationMessage, ImageMessage, VideoMessage, FileMessage))
# def handle_others_message(event):

#     # do only when translation mode is open
#     print('【receive type】', event.message.type)
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text="無法理解呢...本服務目前僅支援文字訊息、語音訊息以及傳送貼圖功能唷！"))     
    
    
if __name__ == "__main__":

    # create tmp dir for download content
    make_dir(TEMP_PATH)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
