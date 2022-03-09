from base64 import urlsafe_b64encode
from email.message import EmailMessage
from typing import Type
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Account
from .forms  import RegistrationForm
from django.contrib import auth,messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import string
import random
from UserProfile.views import create_profile
from UserProfile.models import Profile
from exception_handling.views import log_exception
from exception_handling.models import ExceptionLog

# Create your views here.
def signup(request):
    try:
        custom_user_id = ''.join(random.choices(string.ascii_uppercase+string.digits,k=10))
        print(custom_user_id)
        if request.method=="POST":
            form = RegistrationForm(request.POST)#contain all form values
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                username = form.cleaned_data['username']
                user = Account.objects.create_user(user_id=custom_user_id,first_name=first_name,last_name=last_name,email=email,username=username,password=password)#this method is present in models.py file
                user.save()
                """
                Creating a fresh profile and account
                """
                create_profile(request,user)   
                """
                User activation mail
                """
                current_site = get_current_site(request)
                mail_subject = "Please activate your mingle account"
                message = render_to_string('account_verification_email.html',{
                    'user':user,
                    'domain':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject,message,to=[to_email])
                send_email.send()
                # messages.success(request,"Your account has been created!")
                return redirect('/accounts/login/?command=verification&email='+email)
        else:
            form = RegistrationForm()
        context = {
            'form':form,
        }
        return render(request,'signup.html',context)
    except Exception as e:
        log_exception(request,e,view_name='signup')

"""User Login"""
def login(request):
    try:
        if request.method=="POST":
            email = request.POST['email']
            password = request.POST['password']

            user = auth.authenticate(email=email,password=password)
            if user is not None:
                auth.login(request,user)
                messages.success(request,'You are logged in')
                return redirect('home')
            else:
                messages.error(request,"Invalid login credentials")
                return redirect('login')
        return render(request,'login.html')
    except Exception as e:
        log_exception(request,e,view_name="login")

@login_required(login_url='login')
def logout(request):
    try:
        auth.logout(request)
        messages.success(request,"You are logged out!")
        return redirect('login')
    except Exception as e:
        log_exception(request,e,view_name="logout")

"""
To activate user account 
PARAMS: uidb64 ->
token ->
"""
def activate(request,uidb64,token):
    try:
        try:
            uid=urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Your account is activated")
            return redirect('login')
        else:
            messages.error(request,"Account activation link expired")
            return redirect('signup')
    except Exception as e:
        log_exception(request,e,view_name="activate")

"""
RESET PASSWORD FUNCTIONALITY
"""

def forgot_password(request):
    try:
        if request.method=="POST":
            email = request.POST['email']
            if Account.objects.filter(email=email).exists():
                user = Account.objects.get(email__iexact=email)
                """
                Reset password email
                """
                current_site = get_current_site(request)
                mail_subject = "Reset your mingle password"
                message = render_to_string('reset_password_email.html',{
                    'user':user,
                    'domain':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject,message,to=[to_email])
                send_email.send()
                messages.success(request,"Reset password link has been sent")
                return redirect('login')
            else:
                messages.error(request,"Account does not exist")
                return redirect('login')
        return render(request,"forgot_password.html")
    except Exception as e:
        log_exception(request,e,view_name="forgot_password")

"""
Checking if the user exists
"""
def reset_password_validate(request,uidb64,token):
    try:
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user,token):
            request.session['uid']=uid
            messages.success(request,"Reset your password")
            return redirect('reset_password')
        else:
            messages.error(request,"This link has expired")
            return redirect('login')
    except Exception as e:
        log_exception(request,e,view_name="reset_password_validate")

"""
Updating the password in the model
"""

def reset_password(request):
    try:
        if request.method=="POST":
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password==confirm_password:
                uid = request.session.get('uid')#uid stored in session in reset_password_validate
                user = Account.objects.get(pk=uid)
                user.set_password(password)#password has been resetted
                user.save()
                messages.success(request,"Password reset successfull")
                return redirect('login')
            else:
                messages.error(request,"Password and confirm password must match!")
                return redirect('reset_password')
        else:
            return render(request,"reset_password.html")
    except Exception as e:
        log_exception(request,e,view_name="reset_password")

