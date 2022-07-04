# chat/consumers.py
from datetime import datetime
from email import message
import json
from time import time
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from knox.models import AuthToken
from chat.models import Message
from classes.models import classroom


class ChatConsumer(WebsocketConsumer):
    
    def create_chat(self, id, message, token, timestamp, user_token):
        token=token.replace('"','')
        selectclass = classroom.objects.get(classroom_token = token)
        if 'user' not in self.scope.keys():
            self.scope['user'] = AuthToken.objects.get(token_key=user_token[0:8]).user
        new_msg = Message.objects.create(sender=self.scope['user'], message=message, classroom=selectclass, timestamp=timestamp)
        new_msg.save()

    def get_all_messages(self):
        token = self.scope['url_route']['kwargs']['room_name']
        selectclass = classroom.objects.get(classroom_token = token)
        messages = Message.objects.filter(classroom = selectclass)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)
            
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'fname': message.sender.first_name,
            'lname': message.sender.last_name,
            'message': message.message,
            'timestamp': str(message.timestamp),
        }

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.get_all_messages()


            

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json['message']
        token = text_data_json['token']
        user_token = text_data_json['user_token']
        self.scope['user'] = AuthToken.objects.get(token_key=user_token[0:8]).user


        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'id': self.scope['user'].id,
                'fname': self.scope['user'].first_name,
                'lname': self.scope['user'].last_name,
                'timestamp': str(datetime.now()),
                'token': token,
                'user_token' : user_token
            }
        )
        new_msg = self.create_chat(id, message,token, str(datetime.now()),user_token)

    # Receive message from room group
    def chat_message(self, event):
        if ('message' not in event):
            raise Exception('no message_exception')
        if ('fname' not in event):
            raise Exception('no fname_exception')
        if ('lname' not in event):
            raise Exception('no lname_exception')
        if ('token' not in event):
            raise Exception('no class token_exception')
        message = event['message']
        fname = event['fname']
        lname = event['lname']
        timestamp = event['timestamp']
        id = event['id']
        token = event['token']
        user_token = event['user_token']


        # Send message to WebSocket
        data = {
            'message': message,
            'fname': fname,
            'lname': lname,
            'timestamp': timestamp
        }
        self.send(text_data=json.dumps(data))
        
        