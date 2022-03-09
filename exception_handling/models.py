from django.db import models
from accounts.models import Account

# Create your models here.
class ExceptionLog(models.Model):
    log_id = models.CharField(max_length=250,primary_key=True)
    exception_type = models.CharField(max_length=250)
    exception_message = models.CharField(max_length=250)
    exception_time = models.DateTimeField(auto_now_add=True)
    view_name = models.CharField(max_length=250,default="Empty")
    # user = models.ForeignKey(Account,on_delete=,null=True,blank=True)

    def __str__(self):
        return self.exception_message
