from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)
    
    def __str__(self):
        return self.name


class Chat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chats', null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats', null=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.sender.username}: {self.message}'
