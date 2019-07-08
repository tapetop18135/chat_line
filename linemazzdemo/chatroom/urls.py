from django.urls import path, include

from .views import ChatRoomView
from .api import get_message, get_lazy_message, send_message

app_name = "chat"

urlpatterns = [
    path('chat_one_one/', ChatRoomView.as_view(), name="chatroom"),

    # API
    path("api/get_message/", get_message, name="get_message"),
    path("api/get_lazy_message/", get_lazy_message, name="get_lazy_message"),
    path("api/send_message/", send_message,name="send_message")
]
