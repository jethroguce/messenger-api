from flask import current_app
import requests


class Message(object):
    def __init__(self, message_type, entry):
        self.__message_type = message_type
        self.messages = entry

        self.reply()


    @staticmethod
    def authenticate(verify_token, challenge):
        if challenge and verify_token == current_app.config['FB_VERIFY_TOKEN']:
            return challenge
        return 'Invalid Request or Verification Token'

    @property
    def messages(self):
        return self.__messages

    @messages.setter
    def messages(self, data):
        self.__messages = []
        for message in data:
            content = message['messaging'][0]
            if content.get('message', None) is not None:
                message['type'] = 'text'
            elif content.get('referral', None) is not None:
                message['type'] = 'referral'
            else:
                message['type'] = 'unknown'
            self.__messages.append(message)

    def reply(self):
        for message in self.messages:
            content = message['messaging'][0]
            fb_id = content['sender']['id']
            if message['type'] == 'text':
                text = content['message']['text']
            elif message['type'] == 'referral':
                text = content['referral']['ref']

            self.send_message(fb_id, text)

    def send_message(self, fb_id, message):
        data = {
            'recipient': {'id': fb_id},
            'message': {'text': message}
        }
        token = 'access_token={}'.format(current_app.config['FB_PAGE_TOKEN'])
        url = 'https://graph.facebook.com/v2.6/me/messages?{}'.format(token)
        res = requests.post(url, json=data)
        return res.json()
