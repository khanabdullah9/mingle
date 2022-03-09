from django.contrib import admin
from django.urls import path,include 
from . import views
import exception_handling

urlpatterns = [
    path('error/',include(exception_handling.urls)),
]