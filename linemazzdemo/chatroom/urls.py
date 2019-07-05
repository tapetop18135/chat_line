from django.urls import path, include

from .views import ChatRoomView

urlpatterns = [
    path('chat_one_one/', ChatRoomView.as_view(), name="chatroom")
]
