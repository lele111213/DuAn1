from random import triangular
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
            else:
                await self.close()
        
    
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
    requires = {}
    waiting_user = []
    async def connect(self):
        
        self.room_group_name = 'Waiting_Room'
        self.kieu_ghep = self.scope['url_route']['kwargs']['kieu_ghep']
        print(self.scope['url_route']['kwargs'])
        user = self.scope['user']

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        self.option[self.channel_name] = self.kieu_ghep
        self.waiting_user.append(user)
        if self.kieu_ghep == 3:
            age = self.scope['url_route']['kwargs']['age']
            gender = self.scope['url_route']['kwargs']['gender']
            address = self.scope['url_route']['kwargs']['address']
            self.requires[self.channel_name] = {
                'age': age,
                'gender': gender,
                'addressId': address,
            }

        await self.add_user_channel(user, self.channel_name)
        
        print('--',self.option)
        for wu in self.waiting_user:
            print(wu.username, ':kieu_ghep=' , self.option[wu.channel])


        '''
            kiểm tra điều kiện ghép cặp
            .....
            => kiểm tra điều kiện
            nếu tìm đc phù hợp => vào cùng 1 room chat => leave group
            không tìm được => chờ đến khi có user mới vào
            => kiểm tra điều kiện
        '''
        if len(self.waiting_user) > 1:
            for u in self.waiting_user[0:-1]:
                if u.username != user.username:
                    # Bản thân ghép ngẫu nhiên (1)
                    if self.kieu_ghep==1:
                        # Mục tiêu ghép ngẫu nhiên (1)
                        if self.option[u.channel]==1: 
                            r_id = await self.gep_cap(user, u)
                            await self.send_success(user.channel, u.channel, r_id)
                        else:
                            # mục tiêu ghép gần giống (2)
                            if self.option[u.channel]==2:
                                point_total = await self.total_point(u, user)
                            # Mục tiêu ghép theo tuỳ chọn (3)
                            elif self.option[u.channel]==3:
                                req = self.requires[u.channel]
                                point_total = await self.total_point(req, user, accuracy=True)
                            if point_total==3:
                                r_id = await self.gep_cap(user, u)
                                await self.send_success(user.channel, u.channel, r_id)
                    # Bản thân ghép gần giống (2)
                    elif self.kieu_ghep==2:
                        if self.option[u.channel]==1 or self.option[u.channel]==2:
                            point_total = await self.total_point(u, user)
                        elif self.option[u.channel]==3:
                            req = self.requires[u.channel]
                            point_total = await self.total_point(req, user, accuracy=True)
                        if point_total==3 or point_total==6:
                            r_id = await self.gep_cap(user, u)
                            await self.send_success(user.channel, u.channel, r_id)
                    # Bản thân ghép tuỳ chọn (3)
                    else:
                        req = self.requires[user.channel]
                        point_total = await self.total_point(req, u, accuracy=True)
                        if self.option[u.channel]==3:
                            if point_total == 3:
                                req = self.requires[u.channel]
                                point_total += await self.total_point(req, user, accuracy=True)
                        elif self.option[u.channel]==2:
                            if point_total == 3:
                                point_total += await self.total_point(u, user)
                        if point_total==3 or point_total==6:
                            r_id = await self.gep_cap(user, u)
                            await self.send_success(user.channel, u.channel, r_id)


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

    
    # Receive message from web socket
    async def receive(self, text_data):

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message'
            }
        )


    async def send_success(self, channel1, channel2, room_id):
        print("ghep thanh cong, room id:" , room_id)
        await self.channel_layer.send(channel1,
            {
                'type': 'ghep_thanh_cong',
                'status': '1',
                'message': 'Thành công!',
                'room_id': room_id,
            })
        await self.channel_layer.send(channel2,
            {
                'type': 'ghep_thanh_cong',
                'status': '1',
                'message': 'Thành công!',
                'room_id': room_id,
            })

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


    async def total_point(self, user1, user2, accuracy=False):
        point_total = 0
        point_total += await self.point_address(user1, user2, accuracy)
        point_total += await self.point_age(user1, user2, accuracy)
        point_total += await self.point_gender(user1, user2, accuracy)
        return point_total

    @sync_to_async
    def point_age(self, user1, user2, accuracy=False):
        point = 0
        if not accuracy:
            age_c = abs(int(user1.age.strftime('%Y')) - int(user2.age.strftime('%Y')))
            if age_c <= 3:
                point += 1
        else:
            if user1['age'] == 999:
                return 1
            age_c = user1['age'] - (2021-int(user2.age.strftime('%Y')))
            if age_c == 0:
                point += 1
        return point

    @sync_to_async
    def point_address(self, user1, user2, accuracy=False):
        point = 0
        if accuracy:
            if user1['addressId'] == 999:
                return 1
            address_c = abs(user1['addressId'] - user2.addressId)
        else:
            address_c = abs(user1.addressId - user2.addressId)
        if address_c==0:
            point = 1
        return point

    @sync_to_async
    def point_gender(self, user1, user2, accuracy=False):
        point = 0
        if not accuracy:
            if user1.gender == 'nu' and user2.gender == 'nam':
                point += 1
            elif user1.gender == 'nam' and user2.gender == 'nu':
                point += 1
            elif user1.gender == 'another' and user2.gender == 'another':
                point += 1
        else:
            if user1['gender'] == 'null':
                return 1
            if user1['gender'] == user2.gender:
                point += 1
        return point


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
