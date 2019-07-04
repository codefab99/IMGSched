from channels.generic.websocket import AsyncWebsocketConsumer
from IMGSched.models import Comment, Meeting, Userprofile
from django.contrib.auth.models import User

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):