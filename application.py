import os

import requests
from flask import Flask, request

FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')
FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN')
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/messenger')
def messenger_webhook():
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    print(verify_token)
    if challenge and verify_token == FB_VERIFY_TOKEN:
        return challenge
    return 'Invalid Request or Verification Token'


@app.route('/messenger', methods=['POST'])
def send_message():
    data = request.json
    if data['object'] != 'page':
        return 'Unknown Event'
    for entry in data['entry']:
        messages = entry['messaging']
        message = messages[0]
        if message:
            fb_id = message['sender']['id']
            text = message['message']['text']
            fb_send_message(fb_id, text)
    return 'OK'


def fb_send_message(fb_id, message):
    data = {
        'recipient': {'id': fb_id},
        'message': {'text': message}
    }
    token = 'access_token={}'.format(FB_PAGE_TOKEN)
    url = 'https://graph.facebook.com/v2.6/me/messages?{}'.format(token)
    res = requests.post(url, json=data)
    return res.json()


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
