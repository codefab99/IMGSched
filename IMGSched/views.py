from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import mixins, generics, renderers, viewsets, permissions
from IMGSched.models import Meeting
from IMGSched.serializers import MeetingSerializer, UserSerializer
from django.contrib.auth.models import User
from IMGSched.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Create your views here.

@login_required
def home(request):
    return render(request, 'registration/home.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    This viewset automatically provides 'list' and 'detail' actions.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MeetingViewSet(viewsets.ModelViewSet):
	'''
	    This viewset automatically provides 'list', 'create', 'retrieve',
	    'update' and 'destroy' actions.
	'''
	queryset = Meeting.objects.all()
	serializer_class = MeetingSerializer
	permission_class = (permissions.IsAuthenticatedOrReadOnly,
		IsOwnerOrReadOnly,)

	def perform_create(self, serializer):
		serializer.save(host=self.request.user)

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format = format),
		'meetings': reverse('meeting-list', request=request, format=format)
		})