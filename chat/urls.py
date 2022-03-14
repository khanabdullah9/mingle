from django.urls import path
from . import views

urlpatterns = [
    path('',views.chat,name='chat'),
    path('<str:room_name>',views.room,name='room'),
    path('load_room/<str:partner>',views.load_room,name='load_room'),
    path('room/<str:room_name>/<str:current_user>',views.room,name='room'),
    path('load_with_room_name/<str:room_name>',views.load_with_room_name,name='load_with_room_name'),
]