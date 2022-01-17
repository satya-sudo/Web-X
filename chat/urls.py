from django.urls import path

from . import views

urlpatterns = [
    path('chat/request/<str:phone>/', views.createConnection, name='createConnection'),

    path('chat/requests/recived/', views.getConnectionRequests, name='getConnections'),
    path('chat/requests/sent/',view=views.getSentRequests,),
    path('chat/requests/accept/<str:phone>/',view=views.acceptConnection,),


]