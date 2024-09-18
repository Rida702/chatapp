from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("select_user/", views.select_user, name="select_user"),
    path("chatroom/<str:room_name>/", views.room, name="room"),
]