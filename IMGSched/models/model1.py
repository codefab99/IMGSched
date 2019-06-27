from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django import forms
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.

USER_ROLE = (
    (1, 'NORMAL USER'),
    (2, 'ADMIN')
)
MEETING_CHOICES = (
    (1, 'Public'),
    (2, 'Private')
)

class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	permission_level = models.IntegerField(choices = USER_ROLE)
	def __str__(self):
		return '%s' % (self.user)

def create_profile(sender,**kwargs):
	# create_user(request)
	if kwargs['created']:
		user_profile = UserProfile.objects.create(username=kwargs.get('instance'))		
		user_profile.save()

class Meeting(models.Model):
    created_on = models.DateTimeField()
    meeting_text = models.TextField()
    host_id = models.ForeignKey(User, related_name='host', on_delete=models.CASCADE)
    meeting_type = models.IntegerField(choices=MEETING_CHOICES)
    invited_id = models.ManyToManyField(User, related_name='invitees')
    meeting_time = models.DateTimeField()

    class Meta:
        ordering = ('created_on', )