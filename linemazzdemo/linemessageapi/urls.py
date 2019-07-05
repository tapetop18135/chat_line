from django.urls import path, include

from .views import CallbackView

urlpatterns = [
    path('callback/<int:channel_id>', CallbackView.as_view(), name="callback_line")
]
