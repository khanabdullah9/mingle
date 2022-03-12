from datetime import datetime
from django.db import models
from accounts.models import Account
import datetime

# Create your models here.
class ExceptionLog(models.Model):
    log_id = models.CharField(max_length=250,primary_key=True)
    exception_type = models.CharField(max_length=250)
    exception_message = models.CharField(max_length=250)
    exception_time = models.DateTimeField(default=datetime.datetime.now)
    view_name = models.CharField(max_length=250,default="Empty")

    def __str__(self):
        return self.exception_message
