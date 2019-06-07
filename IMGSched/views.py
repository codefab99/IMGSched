from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

@login_required
def home(request):
    return render(request, 'registration/home.html')

def logout(request):
    auth_logout(request)
    return redirect('/')