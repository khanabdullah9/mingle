from django.shortcuts import render, redirect
from .models import ExceptionLog
import random
import string

# Create your views here.
def log_exception(request,Exception,view_name):
    log_id = ''.join(random.choices(string.ascii_uppercase+string.digits,k=10))
    log = ExceptionLog(log_id=log_id,exception_type=str(type(Exception)),exception_message=str(Exception),view_name=view_name)
    log.save()
    return render(request,"error.html")
