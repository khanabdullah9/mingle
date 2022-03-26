# import pytest
from accounts.models import Account
from .models import ChatRoom, Message
from channels.generic.websocket import WebsocketConsumer
import json
from channels.db import database_sync_to_async
import string
import random
import time
from datetime import datetime
from asgiref.sync import async_to_sync

class ChatRoomConsumer(WebsocketConsumer):

    def fetch_messages(self,message,username,room_name):
        print("fetch_messages() invoked and the room_name is: "+room_name)

    def new_message(self,message,username,room_name):
        print("new_message() invoked!")

    def save_message(self,message,username,room_name):
        chat_id = ''.join(random.choices(string.ascii_uppercase+string.digits,k=10))
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        user = Account.objects.get(username=username)
        room = ChatRoom.objects.get(room_name=room_name)
        new_message = Message(message_id=chat_id,message=message,time=str(current_time),room_name=room,message_sender=user)
        new_message.save()  
        print(f"[SUCCESS] save_message() invoked with message={message}, room_name={room_name} and username={username}")
        self.send_chat_message(message,username,room_name)


    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message,
        'save_message':save_message,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name= 'chat_%s'%self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        room_name = text_data_json['room_name']
        # print("[RECIEVED] "+room_name)
        print("[receiving....]"+message)
        self.commands[text_data_json['command']](self,message,username,room_name)#maybe pass the room_name here

    def send_chat_message(self,message,username,room_name):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chatroom_message',
                'message':message,
                'username':username,
                'room_name':room_name,
            }
        )

    # def send_message(self,message):
    #     self.send(text_data=json.dumps(message))


    def chatroom_message(self,event):
        message = event['message']
        username = event['username']
        room_name = event['room_name']
        print("[SENDING....]"+message)

        room_obj = ChatRoom.objects.get(room_name=room_name)
        sender = Account.objects.get(username=username)

        self.send(text_data=json.dumps({
                'message':message,
                'username':username,
            }))