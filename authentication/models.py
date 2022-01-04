from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,PermissionsMixin, UserManager
import uuid
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class UserManager(BaseUserManager):

    def create(self,phone,username,password=None):
        if not phone:
            raise ValueError('Users must have a phone number')
        user = self.model(phone=phone,username=username)
        user.set_password(password)
        user.save()
        return user



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=11, unique=True,db_index=True)
    username = models.CharField(max_length=50)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username + ' ' + self.phone

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'access': str(refresh.access_token),
        }

    

