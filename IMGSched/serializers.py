from rest_framework import serializers
from IMGSched.models import Meeting
from django.contrib.auth.models import User

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