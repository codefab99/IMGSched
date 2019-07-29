from rest_framework import serializers
from IMGSched.models import Meeting, Comment, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings

User = get_user_model()

class MeetingSerializer(serializers.ModelSerializer):
    host = serializers.ReadOnlyField(source='host_id.first_name')
    invitees = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), many=True, view_name='user-detail')
    class Meta:
        model = Meeting
        fields = ('url', 'created_on', 'host', 'meeting_type', 'meeting_text', 'invitees', 'meeting_time')

class UserSerializer(serializers.ModelSerializer):
    meetings = serializers.HyperlinkedRelatedField(many=True, view_name='meeting-detail', read_only=True)
    meeting_invited = MeetingSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'meeting_invited', 'meetings')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
	    model = UserProfile
	    fields = ('user','permission_level')

    def create(self, validated_data):
	    user_data = validated_data.pop('user')
	    user = UserSerializer.create(UserSerializer(), validated_data=user_data)
	    student, created = UserProfile.objects.update_or_create(user=user, permission_level=validated_data.pop('permission_level'))
	    return student

class CommentSerializer(serializers.ModelSerializer):
    comment_user = serializers.ReadOnlyField(source='user_id.first_name')
    class Meta:
        model = Comment
        fields = ('id', 'time', 'comment_text','comment_user')