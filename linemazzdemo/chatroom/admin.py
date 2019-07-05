from django.contrib import admin

from .models import ChatSession, ChatMessage 


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'token', 'line_account', 'line_contact', 'start_conversation_at', 'end_conversation_at', 'update_conversation_at')
    search_fields   = ['token', 'line_account', 'line_contact']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_filter     = ['line_account', 'line_contact', 'message_type', 'text', 'image', 'file', 'created_on', 'is_read', 'raw_data']
    search_fields   = ['line_account', 'line_contact']
