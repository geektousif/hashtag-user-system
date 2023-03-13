from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reciever')
    message = models.TextField()
    message_time = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"message from {self.sender} to {self.reciever}"
