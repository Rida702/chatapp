from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, Chat

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name']

class ChatSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Chat
        fields = ['id', 'room', 'sender', 'message', 'timestamp']
