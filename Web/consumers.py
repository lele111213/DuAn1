from Web.views import room
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.conf import settings

from .models import ChatRoom, RoomChatMessage, WaitingRoom

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        user = self.scope['user']

        if user.is_authenticated:

            self.room_group_name = 'chat_%s' % self.room_id

            # Join room
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            check = await self.check_user(self.room_id, self.scope['user'])
            if check:
                await self.accept()
        
    
    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        user = self.scope['user']
        await self.remove_user_room(self.room_id ,user)
    
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
            return False
        return True

    @sync_to_async
    def remove_user_room(self, room_id, user):
        room = ChatRoom.objects.filter(id = room_id).first()
        room.remove_user(user)


class GhepConsumer(AsyncWebsocketConsumer):
    option = {}
    waiting_user = []
    async def connect(self):
        
        self.room_group_name = 'Waiting_Room'
        self.kieu_ghep = self.scope['url_route']['kwargs']['kieu_ghep']
        user = self.scope['user']

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.channel_layer.send(self.channel_name,
        {
            'type': 'home_ghep_cap',
            'status': '0',
            'message': 'Đang chờ!'
        })

        self.option[self.channel_name] = self.kieu_ghep
        self.waiting_user.append(user)
        print('--',self.option)
        for wu in self.waiting_user:
            print(wu.username, ':kieu_ghep=' , self.kieu_ghep)
        await self.add_user_channel(user, self.channel_name)
        
        await self.add_room_waiting(user)

        '''
            kiểm tra điều kiện ghép cặp
            .....
            => kiểm tra điều kiện
            nếu tìm đc phù hợp => vào cùng 1 room chat => leave group
            không tìm được => chờ đến khi có user mới vào
            => kiểm tra điều kiện
        '''
        if len(self.waiting_user) > 1:
            for u in self.waiting_user:
                if not u is user:
                    if self.kieu_ghep==1:
                        if self.option[u.channel]==1:
                            r_id = await self.gep_cap(user, u)
                            await self.channel_layer.send(user.channel,
                                    {
                                        'type': 'ghep_thanh_cong',
                                        'status': '2',
                                        'message': 'Thành công!',
                                        'room_id': r_id,
                                    })
                            await self.channel_layer.send(u.channel,
                                    {
                                        'type': 'ghep_thanh_cong',
                                        'status': '2',
                                        'message': 'Thành công!',
                                        'room_id': r_id,
                                    })
                        elif self.option[u.channel]==2:
                            pass
                            # option 2
                        else:
                            pass
                            # option 3
                    elif self.kieu_ghep==2:
                        pass
                    else:
                        pass


    async def home_ghep_cap(self, event):
        status = event['status']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'status': status,
        }))


    async def ghep_thanh_cong(self, event):
        status = event['status']
        message = event['message']
        room_id = event['room_id']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'status': status,
            'room_id': room_id,
        }))
    

    async def disconnect(self, close_code):
        # Leave room
        user = self.scope['user']

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        self.option.pop(user.channel)
        self.waiting_user.remove(user)

        await self.remove_user_channel(user)
        
        await self.leave_room(user)

    
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
    def gep_cap(self, user1, user2):
        chatRoom = ChatRoom()
        chatRoom.save()
        chatRoom.add_user(user1)
        chatRoom.add_user(user2)
        chatRoom.title = f'Room của {user1.fullname} và {user2.fullname}.'
        chatRoom.save()
        user1.room_chat.add(chatRoom)
        user1.room_view.add(chatRoom)
        user2.room_chat.add(chatRoom)
        user2.room_view.add(chatRoom)
        user1.save()
        user2.save()
        room_id = chatRoom.id
        return room_id



    # thêm vào phòng chờ
    @sync_to_async
    def add_room_waiting(self, user):
        room = WaitingRoom.objects.first()
        if not room:
            self.disconnect()
        room.add_user(user)
    
    # Xoá khỏi phòng chờ
    @sync_to_async
    def leave_room(self, user):
        room = WaitingRoom.objects.first()
        if not room:
            self.disconnect()
        room.remove_user(user)

    # add channel_name vào user để tìm user bên trong kênh này (Waiting Room)
    @sync_to_async
    def add_user_channel(self, user, channel):
            user.channel = channel
            user.save()

    # remove channel_name
    @sync_to_async
    def remove_user_channel(self, user):
            user.channel = ""
            user.save()
