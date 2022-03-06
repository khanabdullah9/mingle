from django.db import models
from accounts.models import Account

# Create your models here.
class ChatRoom(models.Model):
    room_id = models.CharField(max_length=250,primary_key=True,default="Empty")
    room_name = models.CharField(max_length=250,unique=True)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    message_id = models.CharField(max_length=250,primary_key=True)
    message = models.CharField(max_length=10000)
    room_name = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    message_time = models.DateTimeField(auto_now_add=True)
    message_sender = models.ForeignKey(Account,on_delete=models.CASCADE)

    def __str__(self):
        return self.message


        
