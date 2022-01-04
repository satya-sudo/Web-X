from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

from .models import User
User = get_user_model()


class PhoneBackEnd(ModelBackend):

    def authenticate(self, request, phone=None, password=None):
        # phone = kwargs['phone']
        # password = kwargs['password']
        try:
            user  = User.objects.get(phone=phone)
            # print(user)
            if user.check_password(password) is True:
                return user
            else:
                return None
        except User.DoesNotExist:
            return None