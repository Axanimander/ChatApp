import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from . import models

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name
        user = self.scope['user'].id
        username = self.scope['user'].username
        user_instance = models.User.objects.get(pk=user)
        room_instance = models.roomModel.objects.get(pk=self.room_name)
        models.chatUser(room=room_instance, user=user_instance, username=username).save()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
    
    def disconnect(self, close_code):
        user = self.scope['user'].id
        username = self.scope['user'].username
        user_instance = models.User.objects.get(pk=user)
        room_instance = models.roomModel.objects.get(pk=self.room_name)
        instance = models.chatUser.objects.filter(user=user, room=room_instance)
        instance.all().delete()
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    def receive(self, text_data):
        user = self.scope['user'].id
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room = text_data_json['roomName']
        roomInstance = models.roomModel.objects.get(pk=room)
        senderInstance = models.User.objects.get(pk=user)
        username = senderInstance.username
        
        logMessage = models.ChatLogMessage.create(room=roomInstance, sender=senderInstance,username=username, content=message)
        logMessage.save()
        async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username']
        print(event)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'username': username,
            'message': message,
        }))