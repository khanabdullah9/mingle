# import pytest
from accounts.models import Account
from .models import ChatRoom, Message
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from channels.testing import HttpCommunicator
from django.test import TestCase
import string
import random
# from asgiref.sync import sync_to_async

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name= 'chat_%s'%self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        room_name = text_data_json['room_name']
        print("[RECIEVED] "+room_name)


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chatroom_message',
                'message':message,
                'username':username,
                'room_name':room_name,
            }
        )

    async def chatroom_message(self,event):
        message = event['message']
        username = event['username']
        room_name = event['room_name']

        #saving the message in the models.
        room_obj = ChatRoom.objects.get(room_name=room_name)
        sender = Account.objects.get(username=username)
        await self.save_message(message=message,sender=sender,room_name=room_obj)

        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
        }))

    @database_sync_to_async
    def save_message(self,message,sender,room_name):
        chat_id = ''.join(random.choices(string.ascii_uppercase+string.digits,k=10))
        new_message = Message(message_id=chat_id,message=message,room_name=room_name,message_sender=sender)
        new_message.save()
