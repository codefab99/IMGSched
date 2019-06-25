from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Meeting(models.Model):
    created_on = models.DateTimeField()
    meeting_text = models.TextField()
    host_id = models.ForeignKey(User, related_name='host', on_delete=models.CASCADE)
    meeting_type = models.CharField(max_length=7, default='public')
    invited_id = models.ManyToManyField(User, related_name='invitees')
    meeting_time = models.DateTimeField()

    class Meta:
        ordering = ('created_on', )