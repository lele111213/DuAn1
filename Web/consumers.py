import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.conf import settings

from .models import ChatRoom, RoomChatMessage

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        user = self.scope['user']

        await self.check_user(self.room_id, self.scope['user'])

        if user.is_authenticated:

            self.room_group_name = 'chat_%s' % self.room_id

            # Join room
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from web socket
    async def receive(self, text_data):

        data = json.loads(text_data)
        message = data['message']
        room_id = data['room']
        mess = None
        mess = await self.save_message(room_id, message)
        message = {
            'content': mess.content,
            'fullname': mess.user.fullname,
            'timestamp': mess.timestamp.strftime('%Y-%m-%d %H:%M'),
            'uimage': mess.user.image.url,
            'username': mess.user.username,
        }
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):

        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def websocket_close():
        pass


    @sync_to_async
    def save_message(self, room_id, message):
        user = self.scope["user"]
        if not user:
            self.disconnect()
        else:
            return RoomChatMessage.objects.create_chat(user=user, room_id=room_id, content=message)


    @sync_to_async
    def check_user(self, room_id, user):
        room = ChatRoom.objects.filter(id = room_id).first()
        userInRoom = room.in_room_chat(user)
        if not userInRoom:
            self.disconnect()


class GhepConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.kieu_ghep = self.scope['url_route']['kwargs']['kieu_ghep']
        user = self.scope['user']
        '''
            kiểm tra điều kiện ghép cặp
            .....
            => kiểm tra điều kiện
            nếu tìm đc phù hợp => vào cùng 1 room chat => leave group
            không tìm được => chờ đến khi có user mới vào
            => kiểm tra điều kiện
        ''' 
        
        self.room_group_name = 'Waiting_Room'

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.add_user_channel(user, self.channel_name)

        await self.add_room_waiting(user)
    
    async def disconnect(self, close_code):
        # Leave room
        await self.leave_room(self.scope['user'])
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from web socket
    async def receive(self, text_data):

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message'
            }
        )

    @sync_to_async
    def add_room_waiting(self, user):
        room = ChatRoom.objects.first()
        if not room:
            self.disconnect()
        room.add_user(user)

    @sync_to_async
    def leave_room(self, user):
        room = ChatRoom.objects.first()
        if not room:
            self.disconnect()
        room.remove_user(user)

    @sync_to_async
    def add_user_channel(self, user, channel):
            user.channel = channel
            user.save()
