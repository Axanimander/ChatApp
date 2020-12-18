from django.urls import path
from django.contrib.auth import views as auth_views

from . import views 



urlpatterns = [
    path('', views.index),
    path('comment/<int:room_id>/', views.addmessage),
    path('login/', auth_views.LoginView.as_view()),
    path('my_logout/', views.logout_view),
    path('register/', views.myregister),
    path('', views.index, name='account-redirect'),
    path('chat/<int:room_id>/', views.room, name='room'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('filter/<str:tag>', views.index, name="tagurl"),
    path('deleteroom/<int:room_id>', views.delete_room),
    path('follow/<int:user_id>', views.follow, name='follow'),
]