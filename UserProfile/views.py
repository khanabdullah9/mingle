from email import message
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Profile,Image,FollowRequest
import random
import string
from accounts.models import Account
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from comment.models import Comment,Reply
from chat.views import create_chat_room,filter,get_or_create_room_name
from chat.models import ChatRoom,Message
import traceback
from exception_handling.views import log_exception
from exception_handling.models import ExceptionLog
from pathlib import Path

# Create your views here.
def create_profile(request,user):
    try:
        custom_profile_id = ''.join(random.choices(string.ascii_uppercase+string.digits,k=10))
        profile = Profile(profile_id=custom_profile_id,user=user,user_follower_count=0,user_following_count=0,bio=None)
        profile.user_has_follower.add(None)
        profile.user_is_following.add(None) 
        profile.save()
    except Exception as e:
        log_exception(request,e,view_name="create_profile")  
        return render(request,"error.html")

"""View own profile"""
# @login_required(login_url='login')
def profile(request):
    try:
        if request.user.is_authenticated:
            auth_user = request.user
        user = Account.objects.filter(email=str(auth_user))
        profile = Profile.objects.filter(user__in=user)
        images = Image.objects.filter(profile_id__in=profile)
        user2 = Account.objects.get(email=str(request.user))
        profile_picture = Image.objects.filter(image_id__exact='pp_'+user2.username) 
        """Checking if the current user is the same as the requested profile user"""
        is_current_user = True
        if images is not None:
            context={
            'user':user,
            'profile':profile,
            'images':images,
            'profile_picture':profile_picture,
            'is_current_user':is_current_user,
            }
        else:
            context = {
            'user':None,
            'profile':None,
            'images':None,
            'profile_picture':None,
            }
        return render(request,"profile.html",context)
    except Exception as e:
        log_exception(request,e,view_name="profile")
        return render(request,"error.html")

"""View other profile"""
"""
PARAMS: user_email -> email of the user the profile belongs to 
"""
@login_required(login_url='login')
def view_profile(request,user_email):
    try:
        user = Account.objects.filter(email=user_email)
        current_user_obj = Account.objects.filter(email=str(request.user))
        profile = Profile.objects.filter(user__in=user)
        if Profile.objects.filter(user__in=user,user_has_follower__in = current_user_obj):
            is_following = True
        else:
            is_following = False
        images = Image.objects.filter(profile_id__in=profile)
        user2 = Account.objects.get(email=user_email)
        profile_picture = Image.objects.filter(image_id__exact='pp_'+user2.username)
        """Checking if the current user is the same as the requested profile user"""
        current_user = request.user
        if current_user == user2.email:
            is_current_user = True
        else:
            is_current_user = False
        context = {
            'user':user,
            'profile':profile,
            'images':images,
            'profile_picture':profile_picture,
            'is_current_user':is_current_user,
            'is_following':is_following,
        }
        return render(request,"profile.html",context)
    except Exception as e:
        log_exception(request,e,view_name="view_profile")
        return render(request,"error.html")

    
"""Update own profile"""
def update_profile(request):
    try:
        #prepopulating the form fields
        user = Account.objects.filter(email=str(request.user))
        profile = Profile.objects.filter(user__in=user)
        user2 = Account.objects.get(email=str(request.user))
        context = {
            'user':user,
            'profile':profile,
        }
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            username = request.POST['username']
            bio = request.POST['bio']
            profile_picture=""
            try:
                profile_picture = request.FILES['profile_picture'] 
                profile_picture_ext = str(profile_picture).split('.')[1]
                if profile_picture_ext=="jpg":
                    user = Account.objects.get(email=str(request.user))
                    profile = Profile.objects.get(user=user)
                    old_custom_profile_id = 'pp_'+user.username
                    new_custom_profile_id = 'pp_'+username
                    #if and only the profile picture exists
                    if Image.objects.filter(image_id=old_custom_profile_id).exists():
                        #deleting previous profile picture
                        delete_image(request,old_custom_profile_id)
                        #decrementing the post count
                        profile.post_count -= 1
                        profile.save()
                    #adding a profile picture
                    image = Image(image_id=new_custom_profile_id,user=user,profile_id=profile,image=profile_picture,image_caption=username,image_liked_count=0)
                    image.image_liked_by.add(None)
                    user.first_name=first_name
                    user.last_name = last_name
                    user.email = email
                    user.username = username
                    user.save()
                    profile.bio = bio
                    image.save()
                    #incrementing the post count
                    profile.post_count+=1
                    profile.save()
                    #setting the profile picture caption to profile bio
                    img = Image.objects.get(image_id='pp_'+username)
                    img.image_caption = profile.bio
                    img.save()
                    messages.success(request,"Profile has been update successfully!")
                    return redirect('profile')
                else:
                    messages.error(request,"You can only upload jpg image")
            except Exception as e:
                messages.error(request,"Profile picture is must!")
    except Exception as e:
        log_exception(request,Exception=e,view_name="update_profile")
        return render(request,"error.html")
    return render(request,"update.html",context)

"""Post in image to gallery"""
def post_image(request):
    try:
        try:
            if request.method=="POST":
                posted_image = request.FILES['posted_image']
                caption = request.POST['caption']
                posted_image_extention = str(posted_image).split('.')[1]
                if posted_image_extention == "jpg":#validating the input
                    if len(caption)>0:
                        user = Account.objects.get(email=str(request.user))
                        profile = Profile.objects.get(user=user) 
                        custom_image_id = ''.join(random.choices(string.ascii_uppercase+string.digits,k=10))     
                        image = Image(image_id=custom_image_id,user=user,profile_id=profile,image=posted_image,image_caption=caption,image_liked_count=0)
                        image.image_liked_by.add(None)
                        image.save()
                        profile.post_count+=1
                        profile.save()
                        messages.success(request,"Image has been posted successfully!")
                    else:
                        messages.warning(request,"Give a nice caption")
                else:
                    messages.warning(request,"You can only select .jpg image")
        except Exception as e:
            messages.warning(request,"Are you forgetting something?")
        return render(request,"post_image.html")
    except Exception as e:
        log_exception(request,e,view_name="post_image")
        return render(request,"error.html")
    
"""Delete image from gallery"""
"""
PARAMS: (string) image_id -> primary key of the image
"""
def delete_image(request,image_id):
    try:
        #deleting image
        image = Image.objects.get(image_id=image_id)
        image.delete()
        #decrementing the post count
        user = Account.objects.get(email=str(request.user))
        profile = Profile.objects.get(user=user)
        if profile.post_count >= 1:
            profile.post_count -= 1
            profile.save()
        #delete all the comments on that image
        image = Image.objects.filter(image_id=image_id)
        comments = Comment.objects.filter(image__in=image).delete()
        return redirect('profile')
    except Exception as e:
        log_exception(request,e,view_name="delete_image")
        return render(request,"error.html")

"""Search user profile functionality"""
def search(request):
    try:
        if request.method=="POST":
            search = request.POST["search"]
            if len(search)<1:
                messages.warning(request,"Enter something!")
            else:
                try:
                    user = Account.objects.get(username=search)
                    if user:
                        user_email = user.email
                        return redirect('view_profile',user_email)  
                except Exception as e:
                    messages.warning(request,"Acount does not exist!")
        query = Account.objects.all()
        all_profiles = []
        for x in query:
            if x.is_admin==False:
                all_profiles.append(x)
        context = {
                'all_profiles':all_profiles,
            }
        # print(all_profiles)
        return render(request,"search.html",context)
    except Exception as e:
        log_exception(request,e,view_name="search")
        return render(request,"error.html")

"""Follow other users"""
"""
PARAMS: follower -> User who wants to follow
"""
def follow(request,follower):
    try:
        follower_user_account = Account.objects.get(email=follower)
        current_user = Account.objects.get(email=str(request.user))
        current_user_profile = Profile.objects.get(user=current_user)
        follower_profile = Profile.objects.get(user=follower_user_account)
        if current_user == follower:
            messages.warning(request,"You cannot follow yourself!")
        else:
            #old followers
            current_user_followers = current_user_profile.user_has_follower.all()
            if follower not in current_user_followers:
                current_user_profile.user_has_follower.add(follower_user_account)
                current_user_profile.user_follower_count+=1
                current_user_profile.save()
                follower_profile.user_is_following.add(current_user)
                follower_profile.user_following_count+=1
                follower_profile.save()
                """Creating a chat room for both the users"""
                create_chat_room(request,follower_user_account.email,current_user.email)
            else:
                messages.warning(request,"You are already following this profile!")
        return redirect('inbox')    
    except Exception as e:
        log_exception(request,e,view_name="follow")
        return render(request,"error.html")

"""Unfollow a user"""
"""
PARAMS: (string) profile -> Profile object of the profile to be unfollowed
"""
def unfollow(request,profile):
    try:
        #checking if the user is following the profile or not
        current_user = Account.objects.get(email=str(request.user))
        current_user_profile = Profile.objects.get(user=current_user)
        profile_owner_email = Account.objects.get(email=profile)
        profile_owner = Account.objects.get(email=profile_owner_email)
        profile_owner_obj = Profile.objects.get(user=profile_owner)
        #removing the profile from the current user
        current_user_profile.user_is_following.remove(profile_owner)
        #decrementing the user following count by 1
        current_user_profile.user_following_count -= 1
        current_user_profile.save()
        #removing the current user from the profile
        profile_owner_obj.user_has_follower.remove(current_user)
        #decrementing the profile follower count by 1
        profile_owner_obj.user_follower_count -= 1
        profile_owner_obj.save()
        #deleting the chat room
        room_name = get_or_create_room_name(request,current_user.username,profile_owner.username)
        # if ChatRoom.objects.filter(room_name=room_name).exists():
        #     chat_room = ChatRoom.objects.get(room_name=room_name)
        #     chat_room.delete()
        #deleting the chatroom messages
        if Message.objects.filter(room_name=room_name).exists():
            msgs = Message.objects.get(room_name=room_name)
            msgs.delete()
        return redirect('view_profile',str(request.user))            
    except Exception as e:
        log_exception(request,e,view_name="unfollow")
        return render(request,"error.html")

"""View the profile user's follower"""
"""
PARAMS: user_email -> email of the user the profile belongs to 
"""
def view_followers(request,user_email):
    try:
       # current_user = request.user
        user = Account.objects.get(email=str(user_email))
        iterable_user = Account.objects.all()
        profile = Profile.objects.get(user=user)
        query = profile.user_has_follower.all()
        profile_follower = []
        for i in query:
            profile_follower.append(i)
        context = {
            'profile':profile,
            'profile_follower':profile_follower,
            'iterable_user':iterable_user,
        }
        return render(request,"viewfollowers.html",context) 
    except Exception as e:
        log_exception(request,e,view_name="view_followers")
        return render(request,"error.html")

"""View who the user is following"""
"""
PARAMS: user_email -> email of the user the profile belongs to 
"""
def view_following(request,user_email):
    try:
        user = Account.objects.get(email=user_email)
        iterable_user = Account.objects.all()
        profile = Profile.objects.get(user=user)
        query = profile.user_is_following.all()
        profile_following = []
        for i in query:
            profile_following.append(i)
        context = {
            'profile':profile,
            'profile_following':profile_following,
            'iterable_user':iterable_user,
        }
        return render(request,"viewfollowing.html",context)
    except Exception as e:
        log_exception(request,e,view_name="view_following")
        return render(request,"error.html")

"""Send a follow request"""
"""
PARAMS: user -> email of the user who has requested to follow
"""
def send_request(request,user):
    try:
        id = ''.join(random.choices(string.ascii_uppercase+string.digits,k=10))
        current_user = Account.objects.get(email=str(request.user))
        user_to_be_followed = Account.objects.get(email=user)
        if current_user != user_to_be_followed:#cannot follow yourself
            #if the requestee object already exists. Just add the requester to the ManyToMany Field
            if FollowRequest.objects.filter(requestee=user_to_be_followed).exists():
                query = FollowRequest.objects.get(requestee=user_to_be_followed)
                current_requests = query.requester.all()
                if current_user not in current_requests:
                    fr = FollowRequest.objects.get(requestee=user_to_be_followed)
                    fr.requester.add(current_user)
                    fr.save()
                    messages.success(request,"Your follow request has been sent!")
                else:
                    messages.warning(request,"Your request is already in the queue!")
            else:#Create a new requestee object.
                if FollowRequest.objects.filter(requestee=user_to_be_followed,requester=current_user).exists()==False:
                    follow_request = FollowRequest(fr_id=id,requestee=user_to_be_followed)
                    follow_request.save()
                    follow_request.requester.add(current_user)
                    messages.success(request,"Your follow request has been sent!")
                else:
                    messages.warning(request,"Your request is already in the queue!")
        return redirect('view_profile',user)
    except Exception as e:
        log_exception(request,e,view_name="send_request")
        return render(request,"error.html")

    
"""Accept user requests"""
"""
PARAMS: follower -> Email of the user whose request has been accepted.
"""
def accept(request,follower):
    try:
        current_user = Account.objects.get(email=str(request.user))
        follower_obj = Account.objects.get(email=follower)
        # print(type(follower_obj))
        follow_request = FollowRequest.objects.get(requestee=current_user)
        follow_request.requester.remove(follower_obj)
        """Delete the follow request from the model and follow the profile"""    
        return redirect('follow',follower)
    except Exception as e:
        log_exception(request,e,view_name="accept")
        return render(request,"error.html")


"""Decline the request"""
"""
PARAMS: follower -> Email of the user whose request has been declined.
"""
def reject(request,follower):
    try:
        current_user = Account.objects.get(email=str(request.user))
        follower = Account.objects.get(email=follower)
        follow_request = FollowRequest.objects.get(requestee=current_user)
        follow_request.requester.remove(follower)   
        return redirect('inbox')
    except Exception as e:
        log_exception(request,e,view_name="reject")
        return render(request,"error.html")

    
"""Redirect to the inbox page"""
def inbox(request):
    try:
        current_user = Account.objects.get(email=str(request.user))
        all_images = Image.objects.all()
        all_request = []
        if FollowRequest.objects.filter(requestee=current_user).exists():
            requests = FollowRequest.objects.get(requestee=current_user)
            query = requests.requester.all()
            for i in query:
                all_request.append(i)
        context = {
            "all_request":all_request,
            "all_images":all_images,
        }
        return render(request,"inbox.html",context)
    except Exception as e:
        log_exception(request,e,view_name="inbox")
        return render(request,"error.html")


"""Delete your own profile"""
def delete_profile(request):
    try:
        if Account.objects.filter(email=str(request.user)).exists():
            current_user = Account.objects.get(email=str(request.user))
            
        """Delete Profile object"""
        if Profile.objects.filter(user=current_user).exists():
            current_user_profile = Profile.objects.get(user=current_user)
            """TO CHANGE THE FOLLOWER'S FOLLOWING COUNT"""

            for a in current_user_profile.user_has_follower.all():
                follower_profile = Profile.objects.get(user=a)
                # follower_following_count = follower_profile.user_following_count#Following count of the user who follow this user
                follower_profile.user_following_count -= 1 # decrementing the following count
                follower_profile.save()

            """TO CHANGE THE FOLLOWER COUNT OF THE USER THIS USER IS FOLLOWING"""
            
            for b in current_user_profile.user_is_following.all():
                following_profile = Profile.objects.get(user=b)#user who this user is following.
                following_profile.user_follower_count -= 1 # decrementing the follower count for each user this user is following.
                following_profile.save()

            current_user_profile.delete()
            
        """Deleting the chat messages"""
        if Message.objects.filter(message_sender=current_user).exists():
            chat_messages = Message.objects.filter(message_sender=current_user)
            chat_messages.delete()
        """Delete Images"""
        if Image.objects.filter(user=current_user).exists():
            images = Image.objects.filter(user=current_user)
            images.delete()
        """Deleting FollowRequest"""
        if FollowRequest.objects.filter(requestee=current_user,requester=current_user).exists():
            follow_requests = FollowRequest.objects.filter(requestee=current_user,requester=current_user)
            follow_requests.delete()
        """Deleting Comments"""
        if Comment.objects.filter(commenter=current_user).exists():
            comments = Comment.objects.filter(commenter=current_user)
            comments.delete()

        """Deleting account object"""
        current_user.delete()
        return redirect('/')
    except Exception as e:
        log_exception(request,e,view_name="delete_profile")
        return render(request,"error.html")


    
