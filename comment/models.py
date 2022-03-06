from django.db import models
from UserProfile.models import Image
from accounts.models import Account

# Create your models here.
class Comment(models.Model):
    comment_id = models.CharField(max_length=250,primary_key=True)
    comment = models.CharField(max_length=300,null=True,blank=True)
    comment_time = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(Image,on_delete=models.CASCADE,null=True,blank=True)
    commenter = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)
    commenter_username = models.CharField(max_length=250,default="Empty")

    def __str__(self):
        return str(self.comment)

class Reply(models.Model):
    reply_id = models.CharField(max_length=250,primary_key=True)
    reply = models.CharField(max_length=300,null=True,blank=True)
    reply_time = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True,blank=True)
    replier = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)
    replier_username = models.CharField(max_length=250,default="Empty")

    def __str__(self):
        return str(self.reply)