import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import ChatRoom,Message
from accounts.models import Account
from UserProfile.models import Profile,Image
import string
import random
import time
from exception_handling.views import log_exception
from django.contrib import messages

# Create your views here.
def chat(request):
    try:
        all_images = Image.objects.all()
        current_user = Account.objects.get(email=str(request.user))
        profile = Profile.objects.get(user=current_user)
        user_following = []
        friends = []
        for a in profile.user_has_follower.all():
            if a not in friends:
                friends.append(a)
        for b in profile.user_is_following.all():
            if b not in friends:
                friends.append(b)
        query = profile.user_is_following.all()
        for i in query:
            user_following.append(i)
        context = {
            'username':current_user.username,
            'user_following':user_following,
            'friends':friends,
            'all_images':all_images,
        }
        return render(request,"chat.html",context)
    except Exception as e:
        log_exception(request,e,view_name="chat")
        return render(request,"error.html")


"""Chat room"""
"""
PARAMS: (string) room_name -> model name of the chat room
(string) current_user -> username of the current logged in user
"""
def room(request,room_name):
    try:
        all_images = Image.objects.all()
        all_users = Account.objects.all()
        room_obj = ChatRoom.objects.get(room_name=room_name)
        room_user_1 = room_obj.room_user_1
        room_user_2 = room_obj.room_user_2
        if room_user_1.username != request.user.username and room_user_2.username != request.user.username:
            return redirect('chat')
        room_messages = Message.objects.filter(room_name=room_obj)
        # room_messages = []
        # all_messages = 
        current_user = Account.objects.get(email=str(request.user))
        profile = Profile.objects.get(user=current_user)
        user_following = []
        friends = []
        for a in profile.user_has_follower.all():
            if a not in friends:
                friends.append(a)
        for b in profile.user_is_following.all():
            if b not in friends:
                friends.append(b)
        query = profile.user_is_following.all()
        for i in query:
            user_following.append(i)
        context={
            'username':current_user.username,
            'room_name':room_name,
            'room_user_1_username':str(room_user_1.username),
            'room_user_2_username':str(room_user_2.username),
            'room_messages':room_messages,
            'user_following':user_following,
            'friends':friends,
            'all_users':all_users,
            'all_images':all_images,
        }
        return render(request,"chat.html",context)
    except Exception as e:
        log_exception(request,e,view_name="room")
        return render(request,"error.html")

    
"""Creating a chat room after a user follows another user """
"""
PARAMS: (string) user1 -> email of the user 
(string) user2 -> email of the user 
"""
def create_chat_room(request,user1,user2):
    try:
        room_id = ''.join(random.choices(string.ascii_uppercase+string.digits,k=10))
        room_name = get_or_create_room_name(request,user1,user2)
        user1_obj= Account.objects.get(email=user1)
        user2_obj= Account.objects.get(email=user2)
        if ChatRoom.objects.filter(room_name=room_name).exists() == False:
            chat_room = ChatRoom(room_id=room_id,room_name=room_name,room_user_1=user1_obj,room_user_2=user2_obj)
            chat_room.save()
        print(f"[SUCCESS] ChatRoom: {room_name} has been created!")
    except Exception as e:
        log_exception(request,e,view_name="create_chat_room")
        return render(request,"error.html")

    

"""Generating room name"""
"""
PARAMS: (string) user1 -> user email 
(string) user2 -> user email 
"""
def get_or_create_room_name(request,user1,user2):
    try:
        user1 = user1.split('@')[0]
        user2 = user2.split('@')[0]
        if len(user1) < len(user2):
            room_name = user1+user2
        elif len(user2) < len(user1):
            room_name = user2+user1
        elif len(user1) == len(user2):
            if ord(user1[0]) < ord(user2[0]):
                room_name = user1+user2
            elif ord(user2[0]) < ord(user1[0]):
                room_name = user2+user1
            elif ord(user1[0]) < ord(user2[0]):
                room_name = user1+user2
        return filter(room_name)
    except Exception as e:
        log_exception(request,e,view_name="get_or_create_room_name")
        return render(request,"error.html")

    

"""Get the chat room using the room name"""
"""
PARAMS: (string) partner -> email of the other chat room user
"""
def load_room(request,partner):
    try:
        current_user = Account.objects.get(email=str(request.user))
        room_name = get_or_create_room_name(request,current_user.email,partner)
        chat_room = ChatRoom.objects.get(room_name=room_name)
        if chat_room.room_user_1 == current_user or chat_room.room_user_2 == current_user:
            # print(current_user)
            return redirect('room',room_name)
        else:
            return redirect('chat')
    except Exception as e:
        log_exception(request,e,view_name="load_room")
        return render(request,"error.html")

"""Load room with room name"""
"""
PARAMS: (string) room_name -> room_name of the ChatRoom
"""
def load_with_room_name(request,room_name):
    try:
        current_user = Account.objects.get(email=str(request.user))
        chat_room = ChatRoom.objects.get(room_name=room_name)
        if chat_room.room_user_1 == current_user or chat_room.room_user_2 == current_user:
            # print(current_user)
            return redirect('room',room_name)
        else:
            return redirect('chat')
    except Exception as e:
        log_exception(request,e,view_name="load_with_room_name")
        return render(request,"error.html")

"""Eliminate all the punctuations"""
"""
PARAMS: (string) text -> room_name
"""
def filter(room_name):
    op= ""
    punctuations = "!@#$.|_"
    for i in room_name:
        if i not in punctuations:
            op+=i
    return op
