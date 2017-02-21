import os
from flask import Flask, request
from requests import post

FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')
FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN')

app = Flask(__name__)


@app.route('/messenger', methods=['GET', 'POST'])
def messenger_webhook():
    if request.method == 'GET':
        verify_token = request.args.get('hub.verify_token')
        print(verify_token)
        if verify_token == FB_VERIFY_TOKEN:
            challenge = request.args.get('hub.challenge')
            return challenge
        else:
            return 'Invalid Request or Verification Token'
    elif request.method == 'POST':
        data = request.json
        if data['object'] == 'page':
            for entry in data['entry']:
                messages = entry['messaging']
                message = messages[0]
                if message:
                    fb_id = message['sender']['id']
                    text = message['message']['text']
                    fb_send_message(fb_id, text)
        else:
            return 'Unknown Event'
        return 'OK'


def fb_send_message(fb_id, message):
    data = {
        'recipient': {'id': fb_id},
        'message': {'text': message}
    }
    token = 'access_token={}'.format(FB_PAGE_TOKEN)
    url = 'https://graph.facebook.com/v2.6/me/messages?{}'.format(token)
    res = post(url, json=data)

    return res.json()


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
