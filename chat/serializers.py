from rest_framework import serializers
from .models import Connections,User,Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','phone']




class ConnectionsSerializer(serializers.ModelSerializer):
    user  = UserSerializer(read_only=True)
    class Meta:
        model = Connections
        fields = ['user']


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'