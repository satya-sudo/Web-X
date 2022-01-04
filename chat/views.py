from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User,Connections,ConnectionRequest,Thread
from .serializers import UserSerializer,ConnectionsSerializer,MessagesSerializer
# Create your views here.

class ConnectionAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ConnectionsSerializer

    def get(self,request):
        user = request.user
        connections = Connections.objects.filter(user=user)
        serializer = self.serializer_class(connections, many=True)
        return Response(serializer.data,status=200)


class GetMessageThread(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessagesSerializer
    def get(self,request,phone):
        user = request.user
        user2 = User.objects.get(phone=phone)
        thread = Thread.objects.find(user,user2)
        if not thread:
            return Response({"message":"such messages","value":False},status=200)
        messages = thread.messages.all()
        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data,status=200)
        

@api_view(['GET'])        
def checkConnection(request,phone):
    user = request.user
    user1 = User.objects.get(phone=phone)
    connections = Connections.objects.filter(user=user)
    if user1 in connections:
        return Response({"message":"Already Connected",'value':True},status=200)
    else:
        return Response({"message":"Not Connected",'value':False},status=200)

@api_view(['GET'])
def createConnection(request,phone):
    user = request.user
    user1 = User.objects.get(phone=phone)
    connections = ConnectionRequest.objects.create(user=user,connection=user1)
    return Response({"message":"Connection Created"},status=200)

@api_view(['GET'])
def acceptConnection(request,phone):
    user = request.user
    user1 = User.objects.get(phone=phone)
    try:
        connections = ConnectionRequest.objects.get(user=user,connection=user1)
    except ConnectionRequest.DoesNotExist:
        return Response({"message":"Connection Request Does Not Exist"},status=200)
    connection_create = Connections.objects.create(user=user,connection=user1)
    connection_create2 = Connections.objects.create(user=user1,connection=user)
    connections.delete()
    return Response({"message":"Connection Accepted"},status=200)