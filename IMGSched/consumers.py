from channels.generic.websocket import AsyncWebsocketConsumer
from IMGSched.models import Comment, Meeting, Userprofile
from django.contrib.auth.models import User
import json

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'comment_%s' % self.room_name
        comment = Comment(comment_text = "", user_id = "")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # Receive message from WebSocket

    async def receive(self,text_data):
        self.user=self.scope["user"]
        comment = Comment(comment_text="", user_id="")
        meeting = Meeting.objects.get(id=self.room_name)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
       
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'comment_message',
                'message': message,
            }
        )
        
        comment.comment_text=message
        comment.user_id=self.user
        comment.id=meeting
        comment.save()
    # Receive message from room group
    async def comment_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )