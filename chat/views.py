import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import ChatRoom,Message
from accounts.models import Account
from UserProfile.models import Profile,Image
import string
import random
import time

# Create your views here.
def chat(request):
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

"""Chat room"""
"""
PARAMS: (string) room_name -> model name of the chat room
"""
def room(request,room_name):
    all_images = Image.objects.all()
    all_users = Account.objects.all()
    room_obj = ChatRoom.objects.get(room_name=room_name)
    room_messages = Message.objects.filter(room_name=room_obj)
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
        'room_messages':room_messages,
        'user_following':user_following,
        'friends':friends,
        'all_users':all_users,
        'all_images':all_images,
    }
    return render(request,"chat.html",context)

"""Creating a chat room after a user follows another user """
"""
PARAMS: (string) user1 -> username 
(string) user2 -> username 
"""
def create_chat_room(request,user1,user2):
    room_id = ''.join(random.choices(string.ascii_uppercase+string.digits,k=10))
    room_name = get_or_create_room_name(request,user1,user2)
    if ChatRoom.objects.filter(room_name=room_name).exists() == False:
        chat_room = ChatRoom(room_id=room_id,room_name=room_name)
        chat_room.save()
    print(f"[SUCCESS] ChatRoom: {room_name} has been created!")
    

"""Generating room name"""
"""
PARAMS: (string) user1 -> user email 
(string) user2 -> user email 
"""
def get_or_create_room_name(request,user1,user2):
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

"""Get the chat room using the room name"""
"""
PARAMS: (string) partner -> email of the other chat room user
"""
def load_room(request,partner):
    current_user = Account.objects.get(email=str(request.user))
    room_name = get_or_create_room_name(request,current_user.email,partner)
    print("[PARTNER]:"+partner)
    # print("")
    return redirect('room',room_name)

"""Load room with room name"""
"""
PARAMS: (string) room_name -> room_name of the ChatRoom
"""
def load_with_room_name(request,room_name):
    print("[Room Name]:",room_name)
    return redirect('room',room_name)
    # return HttpResponse(room_name)
    
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




#def delete_all_friends(first_name):
#     user = Account.objects.get(first_name=first_name)
#     user_profile = Profile.objects.get(user=user)
#     try:
#         if user_profile.user_has_follower.all() is not None:
#             for i in user_profile.user_has_follower.all():
#                 user_profile.user_has_follower.remove(i)
#             user_profile.user_follower_count = 0
#             user_profile.save()
#         if user_profile.user_is_following.all() is not None:
#             for i in user_profile.user_is_following.all():
#                 user_profile.user_is_following.remove(i)
#             user_profile.user_following_count = 0
#             user_profile.save()
#         print("Function exceuted successfully!")
#     except Exception as e:
#         print(e)
    
            
