from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from schedule.models import UserProfile

USER_ROLE = (
        (1, 'NORMAL USER'),
        (2, 'ADMIN')
)	

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ('username','password')

class UserProfileForm(forms.ModelForm):
	class Meta():
		model = UserProfile
		fields = ('permission_level')
