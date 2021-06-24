from django.db import models
from django.conf import settings
# Create your models here.  


class WaitingRoom(models.Model):

    title       = models.CharField(max_length=255, blank=True, default='Waiting for chat')
    users       = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, help_text="user thuoc waiting room")

    def __str__(self):
        return self.title

    def add_user(self, user):
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added 

    def remove_user(self, user):
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed 
    
    def all_user(self):
        qs = self.users.all()
        return qs



class ChatRoom(models.Model):

    # Room title
    title       = models.CharField(max_length=255, blank=True, default='Room chat')

    # all users who are authenticated and viewing the chat
    users       = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, help_text="user thuoc chatroom")

    created_at  = models.DateTimeField(auto_now_add=True)

    view_users  = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, help_text="user only view", related_name='Viewer')


    def __str__(self):
        return self.title

    # Thêm user vào room (user xem được nội dung của roomchat này)
    def add_user(self, user):
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            if not user in self.view_users.all():
                self.view_users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added 

    # remove = user vẫn xem đc nội dung của room này
    def remove_user(self, user):
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            user.room_chat.remove(self)
            user.save()
            is_user_removed = True
        return is_user_removed
    # remove = user ko xem đc nội dung của room này nữa
    def remove_viewer(self, user):
        is_user_removed = False
        if user in self.view_users.all():
            self.view_users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed

    def in_room_chat(self, user):
        if user in self.users.all():
            return True
        return False


    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "ChatRoom-%s" % self.id


class RoomChatMessageManager(models.Manager):

    def create_chat(self, user, room_id, content):
        chat = RoomChatMessage()
        chat.user = user
        chat.room = ChatRoom.objects.filter(id=room_id).first()
        chat.content = content
        chat.save(using=self._db)
        return chat

    def all_chat(self, room):
        qs = self.filter(room=room).order_by("timestamp")
        return qs

class RoomChatMessage(models.Model):
    """
    Chat message created by a user inside a ChatRoom
    """
    user                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room                = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    timestamp           = models.DateTimeField(auto_now_add=True)
    content             = models.TextField(unique=False, blank=False,)

    objects = RoomChatMessageManager()

    def __str__(self):
        return self.content
