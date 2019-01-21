from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import random, os, tempfile, errno
from speech_to_text import *
#from customer_template import create_customer_template
#from testapiai import send_text_to_dialogflow


# function for create tmp dir for download content
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise

            
app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('YOUR ACCESS TOKEN')
# Channel Secret
handler = WebhookHandler('YOUR CAHNNEL SECRET')

if_trigger = False

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    
    # print packet info
    print('==============================================================================')
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
    global if_trigger
 
    # get message content
    msg = event.message.text
    print('【receive type】', event.message.type)
    print('【text content】', msg) 

    if msg == '吃下翻譯布丁':
        if_trigger = True
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='吃下翻譯布丁之後，發現全身似乎充滿神奇的力量！'))
    elif msg == '布丁消化完了':
        if_trigger = False
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='翻譯布丁被消化的差不多了，神奇的力量漸漸退去'))
    elif msg == '翻譯布丁':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='1.輸入『吃下翻譯布丁』開啟功能\n2.輸入『布丁消化完了』關閉功能'))


    

 # handle a event which receive a audio msg
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    global if_trigger
    print('【receive type】', event.message.type)

    # do only when translation mode is open
    if if_trigger==False:
        return

    # download audio file 
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, suffix='.m4a', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        # tempfile_path = tf.name  
        # print(tempfile)
    
    # speech to text 
    recognize_text = speech_to_text(tf.name)
    print('偵測到語音訊息內容: ', recognize_text)

    # when receive a audio message, add speaker name information above
    source_type = event.source.type
    user_id = event.source.user_id
    group_id = event.source.group_id
    if source_type == 'group':
        profile = line_bot_api.get_group_member_profile(group_id, user_id)
        # print(profile.display_name)
        # print(profile.user_id)
        # print(profile.picture_url)
        if recognize_text == '無法辨識內容':
            reponse_text = '【' + profile.display_name + '】說的話實在是無法翻譯呢...' 
        else:
            reponse_text = '【' + profile.display_name + '】說：\r' + recognize_text
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reponse_text)) 
        
    else: # source_type == 'user' or others
        if recognize_text == '無法辨識內容':
            reponse_text = '您說的話實在是無法翻譯呢...'         
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=recognize_text))  
 
 # handle a event which receive a sticker
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print('【receive type】', event.message.type)

    # do only when translation mode is open
    if if_trigger==False:
        return

    # random choose a sticker to send
    sid = random.randint(1,10)
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=1,
            sticker_id=sid)
    )     

 # handle a event which receive others msg
@handler.add(MessageEvent, message=(LocationMessage, ImageMessage, VideoMessage, FileMessage))
def handle_others_message(event):

    # do only when translation mode is open
    if if_trigger==False:
        return
        
    print('【receive type】', event.message.type)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="無法理解呢...本服務目前僅支援文字訊息、語音訊息以及傳送貼圖功能唷！"))     
    
    
if __name__ == "__main__":

    # create tmp dir for download content
    make_static_tmp_dir()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)