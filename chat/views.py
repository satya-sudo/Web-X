from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import User,Connections,ConnectionRequest,Thread
from .serializers import UserSerializer,ConnectionsSerializer,MessagesSerializer,ConnectionRequestSerializer
# Create your views here.

# class ConnectionAPI(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ConnectionsSerializer

#     def get(self,request):
#         user = request.user
#         connections = Connections.objects.filter(user=user)
#         serializer = self.serializer_class(connections, many=True)
#         return Response(serializer.data,status=200)


# class GetMessageThread(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = MessagesSerializer
#     def get(self,request,phone):
#         user = request.user
#         user2 = User.objects.get(phone=phone)
#         thread = Thread.objects.find(user,user2)
#         if not thread:
#             return Response({"message":"such messages","value":False},status=200)
#         messages = thread.messages.all()
#         serializer = self.serializer_class(messages, many=True)
#         return Response(serializer.data,status=200)
        

# @api_view(['GET'])        
# def checkConnection(request,phone):
#     user = request.user
#     user1 = User.objects.get(phone=phone)
#     connections = Connections.objects.filter(user=user)
#     if user1 in connections:
#         return Response({"message":"Already Connected",'value':True},status=200)
#     else:
#         return Response({"message":"Not Connected",'value':False},status=200)



# api to create a connection 
# that is to make a connection request
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def createConnection(request,phone):
    user = request.user
    try:
        user1 = User.objects.get(phone=phone)
    except User.DoesNotExist:
        return Response({"message":"User does not exist",'status':400},status=400)

    if user == user1:
        return Response({"message":"You cannot connect to yourself",'status':400},status=400)

    connections = Connections.objects.filter(user=user,connection=user1)

    if connections:
        return Response({"message":"Already Connected",'value':True,'status':200},status=200)
    
    connection_request = ConnectionRequest.objects.filter(user=user,connection=user1)
    if connection_request:
        return Response({"message":"Already Requested",'value':True,'status':200},status=200)

    connection_request = ConnectionRequest.objects.create(user=user,connection=user1)
    return Response({"message":"Requested",'value':True,'status':201},status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getConnectionRequests(request):
    user = request.user
    connection_requests = ConnectionRequest.objects.filter(connection=user)
    serializer = ConnectionRequestSerializer(connection_requests, many=True)
    return Response(serializer.data,status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSentRequests(request):
    user = request.user
    connection_requests = ConnectionRequest.objects.filter(user=user)
    serializer = ConnectionRequestSerializer(connection_requests, many=True)
    return Response(serializer.data,status=200)


# api to accept a connection request
# that is to accept a connection request
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def acceptConnection(request,phone):
    user = request.user
    try:
        user1 = User.objects.get(phone=phone)
    except User.DoesNotExist:
        return Response({"message":"User does not exist",'status':400},status=400)
    try:
        connectionRequest = ConnectionRequest.objects.get(user=user1,connection=user)
    except ConnectionRequest.DoesNotExist:
        return Response({"message":"Connection Request Does Not Exist",'status':400},status=400)

    connection_create = Connections.objects.create(user=user,connection=user1)
    connection_create2 = Connections.objects.create(user=user1,connection=user)
    connectionRequest.delete()
    return Response({"message":"Connection Accepted",'status':201},status=200)