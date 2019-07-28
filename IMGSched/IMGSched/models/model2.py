from django.db import models
from django.contrib.auth.models import User
from .model1 import Meeting

class Comment(models.Model):
    user_id = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    time = models.DateTimeField()
    meeting_id = models.ForeignKey(Meeting, related_name='meeting', on_delete=models.CASCADE)
    comment_text = models.TextField()

    class Meta:
        ordering = ('time', )