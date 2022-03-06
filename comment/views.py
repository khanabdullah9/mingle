from email import message
from django.shortcuts import render,redirect
from UserProfile.models import Profile,Image
from accounts.models import Account
import random
import string
from datetime import datetime
from .models import Comment,Reply
from django.contrib import messages


# Create your views here.
"""Redirect to the view_image page"""
"""
PARAMS: image_id:model id of the image
"""
def view_image(request,image_id):
    image_user = Image.objects.get(image_id=image_id)
    # user = Account.objects.filter(email=str(request.user))
    user = Account.objects.filter(email=image_user.user)
    profile = Profile.objects.filter(user__in=user)
    image = Image.objects.filter(profile_id__in=profile,image_id__exact=image_id)
    comment = Comment.objects.filter(image__in=image)
    reply = Reply.objects.filter(comment__in=comment)
    username = Account.objects.all()
    all_images = Image.objects.all()
    context = {
        'user':user,
        'image':image,
        'profile':profile,
        'comment':comment,
        'reply':reply,
        'username':username,
        'all_images':all_images,
        }
    return render(request,"view_image.html",context)

"""Post a comment to that image"""
"""
PARAMS: image_id:model id of the image
"""
def comment(request,image_id):
    custom_comment_id = ''.join(random.choices(string.ascii_uppercase+string.digits,k=10))
    image = Image.objects.get(image_id=image_id)
    user = Account.objects.get(email=str(request.user))
    if request.method=="POST":
        comment_text = request.POST['comment_text']
        if len(str(comment_text))>=1:
            comment = Comment(comment_id=custom_comment_id,comment=comment_text,image=image,commenter=user,commenter_username=user.username)
            comment.save()
        else:
            messages.warning(request,"Maybe you forgot to type something")
    return redirect('view_image',image_id=image_id)
        

"""Reply to a comment"""
"""
PARAMS: image_id:model id of the image
"""
def reply(request,comment_id,image_id):
    print(comment_id+"\n"+image_id)
    if request.method=="POST":
        reply_text = request.POST['reply_text']
        custom_reply_id = ''.join(random.choices(string.ascii_uppercase+string.digits,k=10))
        user = Account.objects.get(email=str(request.user))
        comment = Comment.objects.get(comment_id=comment_id)
        if len(reply_text)>=1:
            reply = Reply(reply_id=custom_reply_id,reply=reply_text,comment=comment,replier=user,replier_username=user.username)
            reply.save()
        else:
            messages.warning(request,"Maybe you forgot to type somthing")
        
    return redirect('view_image',image_id=image_id)

"""Increment the image_liked_count by 1 and saving the liker object"""
"""
PARAMS: image_id->model id of the image
"""
def like(request,image_id):
    if request.method == "POST":
        image = Image.objects.get(image_id=image_id)
        image.image_liked_count+=1
        image.image_liked_by.add(request.user)
        image.save()

    return redirect('view_image',image_id=image_id)


