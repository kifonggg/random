from chatbot_functions import coolbot 
import requests
import os
from flask import Flask, request
import json
import sys
from datetime import datetime

app = Flask(__name__)

acc = os.environ['acc']
sec = os.environ['sec']
verify_token = os.environ['verify_token']
bot = coolbot(acc, sec)
bot_user_id = '466965580757797'


@app.route('/', methods = ['GET'])
def vertify_token():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == verify_token:
            return 'Verification token mismatch', 403
        return request.args['hub.challenge'], 200

    return 'Hello world', 200


@app.route('/', methods = ['POST'])
def webhook():

    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('mentions'):
                    for mentions_list in messaging_event['mentions']:
                        
                        if mentions_list['id'] == bot_user_id:
                            sender_id = messaging_event['sender']['id']
                            thread_id = messaging_event['thread']['id']
                            message_text = messaging_event['message']['text']
                            user_info = bot.get_user_info(sender_id, ['name'])

                            send_result = reply_message(recipient_id = thread_id, content = 'Hi {} , can you calling me?'.format(user_info['name']), message_type = 'thread')                
                            log(send_result)
                elif not(messaging_event.get('thread')):
                    sender_id = messaging_event['sender']['id']
                    
                    if messaging_event.get('message'):
                        message_text = messaging_event['message']['text']
                    elif messaging_event.get('postback'):
                        message_text = messaging_event['postback']['payload']
                        
                    button_type = ['postback', 'postback', 'postback']
                    button_title = ['Metrics Value', 'Metrics Definition', 'Subscription Setting']
                    button_payload = ['Metrics Value', 'Metrics Definition', 'Subscription Setting']
                    button_text = 'Hi, what would you like to get from me?'
                    reply_json = {
                            'message_format': 'button',
                            'type': button_type,
                            'title': button_title,
                            'payload': button_payload,
                            'text': button_text
                    }

                    send_result = reply_message(recipient_id = sender_id, content = reply_json, message_type = 'message')
                    log(send_result)

    return "Done"

            
def reply_message(recipient_id, content, message_type):
    #content['message_format'] = ['text', 'button', 'quick_reply', 'attachemnt']

    if content['message_format'] == 'text':
        log('sending message to {recipient}: {text}'.format(recipient=recipient_id, text=content))
        r = bot.send_text_message(recipient_id = recipient_id, message = content['text'], message_type = message_type)

    elif content['message_format'] == 'button':
        log('sending button message to {recipient}: {text}'.format(recipient=recipient_id, text=content))
        r = bot.send_button_message(recipient_id = recipient_id, message = content['text'], button_type = content['type'], button_titles = content['title'], payload = content['payload'], message_type = message_type)

    elif content['message_format'] == 'quick_reply':
        log('sending quick reply message to {recipient}: {text}'.format(recipient=recipient_id, text=content))
        r = bot.send_quick_reply_message(recipient_id = recipient_id, message = content['text'], content_type = content['type'], reply_titles = content['title'], payload = content['payload'], message_type = message_type)

    elif content['message_format'] == 'attachemnt':
        log('sending attachemnt to {recipient}: {text}'.format(recipient=recipient_id, text=content))
        r = bot.send_text_message(recipient_id = recipient_id, message = content['text'], message_type = message_type)

    return r
    

def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        #else:
        #    msg = unicode(msg).format(*args, **kwargs)
        print('{}: {}'.format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()
    return "Done"



if __name__ == "__main__":
    app.run(debug=True)
