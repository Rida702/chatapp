from django.urls import path
from . import views

"""
urlpatterns = [
    path("select_user/", views.select_user, name="select_user"),
    path("chat/room/<str:room_name>/", views.room, name="room"), 
]
"""

urlpatterns = [
    path('rooms/', views.RoomListCreateView.as_view(), name='room-list-create'),
]