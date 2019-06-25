from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    user_id = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, )
    time = models.DateTimeField()
    meeting_id = models.ForeignKey(Meeting, related_name='meeting')
    comment_text = models.TextField()

    class Meta:
        ordering = ('time', )