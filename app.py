import chatbot_fucntions
import requests
import os
from flask import Flask, request


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
        for messaging_event in entry['messaging']:
            if messaging_event.get('message'):
                sender_id = messaging_event['sender']['id']
                message_text = messaging_event['message']['text']

                send_result = reply_message(recipient_id = sender_id, content = 'Hello World!', message_type = 'message')
                log(send_result)

            if (messaging_event.get('mentions')) & (messaging_event['mentions']['id'] == bot_user_id) :
                sender_id = messaging_event['sender']['id']
                thread_id = messaging_event['thread']['id']
                message_text = messaging_event['message']['text']
                user_info = bot.get_user_info('sender_id', ['name'])

                send_result = reply_message(recipient_id = thread_id, content = '@{} , can you calling me?'.format(user_info['name']), message_type = 'thread')                
                log(send_result)

def reply_message(recipient_id, content, message_type):
    log('sending message to {recipient}: {text}'.format(recipient=recipient_id, text=content))
    bot.send_text_message(recipient_id = recipient_id, message = content, message_type = 'message')
    

def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()



if __name__ == "__main__":
    app.run(debug=True)
