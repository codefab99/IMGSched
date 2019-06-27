from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from rest_framework import mixins, generics, renderers, viewsets, permissions, status
from IMGSched.models import Meeting, Comment, UserProfile
from IMGSched.serializers import MeetingSerializer, UserSerializer, CommentSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from IMGSched.permissions import IsOwnerOrAdmin, IsOwner
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

@login_required
def home(request):
    return render(request, 'registration/home.html')

@login_required
def profile(request):
	meeting = Meeting.objects.all()
	args = {'user': request.user, 'meeting':meeting}
	return render(request, 'profile.html', args)

class UserViewSet(generics.ListCreateAPIView):
    permission_classes = (IsOwner, )
    queryset = UserProfile.objects.all()
    serializer_class= UserProfileSerializer

class UserDetail(APIView):
	permission_classes = (IsOwner,)
	def get_object(self, pk):
		return UserProfile.objects.get(pk=pk)

	def get(self, request, pk, format=None):
		user = self.get_object(pk)
		serializer = UserProfileSerializer(user)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		user = self.get_object(pk)
		serializer = UserProfileSerializer(user)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, format=None):
		user = self.get_object(pk)
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class MeetingViewSet(generics.ListCreateAPIView):
	permission_classes = (IsOwnerOrAdmin, )
	queryset = Meeting.objects.all()
	serializer_class = MeetingSerializer
	
	def get(self, request, format=None):
		meetings = Meeting.objects.all().filter(invitees=request.user.id)
		serializer = MeetingSerializer(meetings, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = MeetingSerializer(data=request.data)
		if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeetingDetail(APIView):
	permission_classes = (IsOwnerOrAdmin, )
	def get_object(self, pk):
		return Meeting.objects.get(pk=pk)

	def get(self, request, pk, format=None):
		meeting = self.get_object(pk)
		serializer = MeetingSerializer(meeting)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		meeting = self.get_object(pk)
		serializer = MeetingSerializer(meeting)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, format=None):
		meeting = self.get_object(pk)
		meeting.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class CommentView(APIView):
	def get_object(self, fk):
		return Comment.objects.get(comment_id=fk)
	def get(self,request,fk,format=None):
		comment=self.get_object(fk)
		serializer=CommentSerializer(comment)
		return Response(serializer.data)

	def delete(self,request,fk,format=None):
		comment=self.get_object(fk)
		comment.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format = format),
		'meetings': reverse('meeting-list', request=request, format=format),
		'comments' : reverse('comment-list', request=request, format=format)
		})

@login_required
def create_event(request):
	service = build_service(request)
	meeting = Meeting.objects.latest('id')
	event = service.events().insert(calendarId='primary', body={
		'summary': meeting.purpose,
        'description' : meeting.detail,
        'start': {'dateTime': meeting.datetime.isoformat()},
        'end': {'dateTime': meeting.datetime.isoformat()},
	}).execute()
	return HttpResponse("Meeting added.")