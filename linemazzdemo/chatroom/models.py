from django.db import models

# Create your models here.
from linemessageapi.models import LineAccounts, LineContact

class ChatSession(models.Model):
    token                   = models.CharField(max_length=1000, db_index=True, unique=True)
    line_account            = models.ForeignKey(LineAccounts, null=True, on_delete=models.SET_NULL)
    line_contact            = models.ForeignKey(LineContact, null=True, on_delete=models.SET_NULL)
    start_conversation_at   = models.DateTimeField(auto_now_add=True)
    end_conversation_at     = models.DateTimeField(blank=True, null=True)
    update_conversation_at  = models.DateTimeField(auto_now=True)
    

class ChatMessage(models.Model):
    line_account    = models.ForeignKey(LineAccounts, null=True, on_delete=models.SET_NULL)
    line_contact    = models.ForeignKey(LineContact, null=True, on_delete=models.SET_NULL)
    message_type    = models.CharField(max_length=1000, db_index=True)
    text            = models.TextField(blank=True)
    image           = models.ImageField(blank=True, null=True, max_length=1000)
    file            = models.FileField(blank=True, null=True, max_length=1000)
    created_on      = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read         = models.BooleanField(default=False)
    # is_push       = models.BooleanField(default=False, db_index=True)
    raw_data        = models.TextField(blank=True, null=True)
    status_coversation      = models.CharField(max_length=20, blank=True)
    

