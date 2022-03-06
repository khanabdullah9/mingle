from django.urls import path
from . import views

urlpatterns = [
    path('',views.profile,name='profile'),
    path('post_image/',views.post_image,name="post_image"),
    path('update_profile/',views.update_profile,name="update_profile"),
    path('search',views.search,name='search'),
    path('view_profile/<str:user_email>',views.view_profile,name='view_profile'),
    path('delete_image/<str:image_id>',views.delete_image,name='delete_image'),
    path('follow/<str:follower>',views.follow,name='follow'),
    path('view_followers/<str:user_email>',views.view_followers,name='view_followers'),
    path('view_following/<str:user_email>',views.view_following,name='view_following'),
    path('unfollow/<str:profile>',views.unfollow,name='unfollow'),
    path('send_request/<str:user>',views.send_request,name='send_request'),
    path('accept/<str:follower>',views.accept,name='accept'),
    path('reject/<str:follower>',views.reject,name='reject'),
    path('inbox/',views.inbox,name='inbox'),
]