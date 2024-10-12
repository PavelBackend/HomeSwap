from django.db import models
from django.urls import reverse
from users.models import Users

class Message(models.Model):
    sender = models.ForeignKey(Users, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Users, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    