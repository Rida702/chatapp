from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)

    def __str__(self):
        return self.name


class Chat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chats', null=True)
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats', null=True)
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats', null=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user_1.username} to {self.user_2.username}: {self.message}'
