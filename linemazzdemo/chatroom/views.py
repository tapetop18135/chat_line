from django.shortcuts import render
from django.http import JsonResponse

from django.views import View

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ChatSession, ChatMessage


class ChatRoomView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        token = request.GET.get('token')
        session_list = ChatSession.objects.filter(token= token)
        if not session_list:
            return JsonResponse({"error": "dont have session"})
        session_list = session_list.filter(end_conversation_at=None)
        if not session_list:
            return JsonResponse({"error": "session is expire"})
        session_now = session_list.first()
        return render(request, 'chatroom/chatroom_.html', context= {"token": token})
