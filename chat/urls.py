from django.urls import path
from . import views

urlpatterns = [
    path("select_user/", views.select_user, name="select_user"),
    path("chat/room/<str:room_name>/", views.room, name="room"),
    #path("chat/group/", views.create_group, name="create_group"),  
]