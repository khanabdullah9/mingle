from django.urls import path
from . import views

urlpatterns = [
    path('view_image/<str:image_id>',views.view_image,name="view_image"),
    path('comment/<str:image_id>',views.comment,name='comment'),
    path('reply/<str:comment_id>/<str:image_id>',views.reply,name='reply'),
    path('like/<str:image_id>',views.like,name='like'),
]