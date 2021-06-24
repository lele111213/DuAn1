from re import T
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.fields.related import ManyToManyField
from Web.models import ChatRoom


class UserManager(BaseUserManager):
    
    def create_user(self, username, password=None, fullname=None, is_active=True, is_staff=False, age="1999-08-09", is_admin=False, phonenumber="", addressId=0, height=170, addressName="TP Hồ Chí Minh", gender="another", hobbies="", image="/images/default.jpg"):
    
        """
        Creates and saves a User.
        """
        if not username:
            raise ValueError('Users must have an username address')
        if not password:
            raise ValueError('User must have a password')
        if not fullname:
            raise ValueError('User must have full name')
        user_obj = User(username=username)

        user_obj.set_password(password)
        user_obj.fullname = fullname
        user_obj.phonenumber = phonenumber
        user_obj.addressId = addressId
        user_obj.addressName = addressName
        user_obj.gender = gender
        user_obj.age = age
        user_obj.height = height
        user_obj.hobbies = hobbies
        user_obj.image = image
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username, fullname, password):
        """
        Creates and saves a staff user with the given username and password.
        """
        user = self.create_user(
            username,
            password=password,
            fullname=fullname,
            is_staff=True
        )
        return user

    def create_superuser(self, username, fullname, password):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(
            username,
            password=password,
            fullname=fullname,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=255,unique=True,verbose_name='username')
    fullname = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=15, blank=True)
    addressId = models.IntegerField(blank=True, default=0)
    addressName = models.CharField(max_length=255, blank=True, default="T.P Hồ Chí Minh")
    gender = models.CharField(max_length=10, blank=True, default="another")
    age = models.DateField(blank=True, default='1999-08-09')
    height = models.IntegerField(blank=True, default=170, verbose_name="Chiều cao (cm)")
    hobbies = models.CharField(max_length=255, blank=True, default="")
    image = models.ImageField(upload_to='images', default='/images/default.jpg', blank=True)
    channel = models.CharField(max_length=255, blank=True, default="")
    room_chat = ManyToManyField(ChatRoom, blank=True, help_text="user thuoc chatroom")
    room_view = ManyToManyField(ChatRoom, blank=True, help_text="user only view", related_name='Viewer')
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname'] # username & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their fullname
        return self.fullname

    def get_short_name(self):
        # The user is identified by their username
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
