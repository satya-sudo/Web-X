from django.db import models
import uuid
from authentication.models import User

# Create your models here.

class Message(models.Model):
    channel_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    thread = models.ForeignKey(User, on_delete=models.CASCADE,related_name="messages")
    timestamp = models.DateTimeField(auto_now_add=True)

class Connections(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="connections")
    connection = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connection')
    room_id = models.CharField(max_length=200,unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class ConnectionRequest(models.Model):  
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    connection = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connection_request')
    timestamp = models.DateTimeField(auto_now_add=True)

class ThreadManager(models.Manager):
    def get_or_new(self,user1,user2,channel_id):
        thread = None
        try:
            thread = self.get(user1=user1,user2=user2,channel_id=channel_id)
        except:
            pass
        try:
            thread = self.get(user1=user2,user2=user1,channel_id=channel_id)
        except: 
            pass
        if not thread:
            thread = self.create(user1=user1,user2=user2,channel_id=channel_id)
        return thread
    def find(self,user1,user2,channel_id):
        thread = None
        try:
            thread = self.get(user1=user1,user2=user2)
        except:
            pass
        try:
            thread = self.get(user1=user2,user2=user1)
        except: 
            pass
        try:
            thread = self.get(channel_id=channel_id)
        except:
            pass
            
        return thread


class Thread(models.Model):
    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel_id = models.CharField(max_length=50, unique=True,db_index=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    @property
    def users(self):
        return [self.user1,self.user2]
    
    @property
    def room_name(self):
        return self.channel_id
    
    def __str__(self) -> str:
        return self.channel_id

