from flask import request, make_response
from flask_restful import Resource, reqparse

from .model import Message


class MessageHandler(Resource):
    def __init__(self):
        self.__reqparse = reqparse.RequestParser()
        if request.method in ('GET'):
            self.__reqparse.add_argument('hub.verify_token', type=str, location='args', dest='verify_token', required=True)
            self.__reqparse.add_argument('hub.challenge', type=str, location='args', dest='challenge', required=True)
        elif request.method in ('POST'):
            self.__reqparse.add_argument('object', type=str, location='json', required=True, dest='message_type',  choices=('page'))
            self.__reqparse.add_argument('entry', type=dict, location='json', required=True, action='append')
        self.__args = self.__reqparse.parse_args()

    def get(self):
        retval = Message.authenticate(**self.__args)
        return make_response(retval)

    def post(self):
        message = Message(**self.__args)
        retval = {
            'status': 'SUCCESS',
            'message': 'Received'
        }
        return retval
