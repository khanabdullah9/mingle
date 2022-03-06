from distutils.command.upload import upload
from email.policy import default
from django.db import models
from accounts.models import Account

class Profile(models.Model):
    profile_id = models.CharField(max_length=250,primary_key=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=False,default="Empty")

    """Users who follow this user"""
    user_follower_count = models.IntegerField(default=0)
    user_has_follower = models.ManyToManyField(Account,null=True,blank=True,related_name="some_random_string_1")

    """Users who this user follows"""
    user_following_count = models.IntegerField(default=0)
    user_is_following = models.ManyToManyField(Account,null=True,blank=True,related_name="some_random_string_2")

    post_count = models.IntegerField(default=0)
    
    bio = models.CharField(max_length=500,null=True,blank=True,default="Empty")
    
    def __str__(self):
        return str(self.user)

class Image(models.Model):
    image_id = models.CharField(max_length=250,primary_key=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=False,default="Empty")
    profile_id = models.ForeignKey(Profile,on_delete=models.CASCADE,null=False,default="Empty")
    image = models.ImageField(upload_to="photos/posts")
    image_caption = models.CharField(max_length=250)
    image_liked_count = models.IntegerField(default=0)
    image_liked_by = models.ManyToManyField(Account,null=True,blank=True,related_name="some_random_string_3")

    def __str__(self):
        return str(self.image_id)

class FollowRequest(models.Model):
    fr_id = models.CharField(max_length=250,primary_key=True)
    """The one who is requested"""
    requestee = models.ForeignKey(Account,on_delete=models.CASCADE)
    """The one who is requesting"""
    requester = models.ManyToManyField(Account,null=True,blank=True,related_name="requestee")

    def __str__(self):
        return str(self.requestee)
    
    