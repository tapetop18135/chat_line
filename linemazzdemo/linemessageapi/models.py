from django.db import models
from linebot.models import SourceRoom, SourceUser, SourceGroup
import requests

class LineAccountTag(models.Model):
    name             = models.CharField(max_length=255, unique=True, db_index=True)
    priority         = models.PositiveIntegerField(help_text='For sorting', default=0, db_index=True)

    def __str__(self):
        return self.name


class LineAccounts(models.Model):
    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.channel_id

    nickname             = models.CharField(blank=True, max_length=50)
    channel_id           = models.CharField(max_length=50, db_index=True)
    channel_access_token = models.TextField()
    channel_secret       = models.CharField(max_length=50)

    created_on           = models.DateTimeField(auto_now_add=True)
    updated_on           = models.DateTimeField(auto_now=True)
    active               = models.BooleanField(default=True)
    is_verify_webhook    = models.BooleanField(default=False)
    line_account_tag     = models.ManyToManyField('LineAccountTag', blank=True, related_name='line_accounts')

    def getProfile(self, source):
        contact_list = LineContact.objects.filter(contact_id=source.user_id)
        if not contact_list:
                if isinstance(source, SourceUser):
                    url = 'https://api.line.me/v2/bot/profile/{userId}'.format(userId=source.user_id)

                headers = {
                    'Authorization': 'Bearer {}'.format(self.channel_access_token), 
                    'Content-type': 'application/json',
                }
                response      = requests.get(url, headers=headers)
                response_json = response.json()
                display_name  = response_json["displayName"]
                contact_now = LineContact(
                    channel = self,
                    contact_id = response_json["userId"],
                    contact_type = LineContact.TYPE_USER,
                    display_name = display_name
                )
        else:
            contact_list_new = contact_list.filter(channel=self)
            if not contact_list_new :
                contact_temp = contact_list[0]
                contact_now = LineContact(
                    channel = self,
                    contact_id = str(contact_temp["contact_id"]),
                    contact_type = LineContact.TYPE_USER,
                    display_name = str(contact_temp["display_name"])
                )
            else:
                contact_now = contact_list_new.first()
        contact_now.save()
        return contact_now




class LineContactManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().exclude(contact_id='Udeadbeefdeadbeefdeadbeefdeadbeef')


class LineContact(models.Model):

    TYPE_USER    = 'user'
    TYPE_GROUP   = 'group'
    TYPE_ROOM    = 'room'
    TYPE_CHOICES = (
        (TYPE_USER, 'User'),
        (TYPE_GROUP, 'Group'),
        (TYPE_ROOM, 'Room'),
    )

    channel         = models.ForeignKey(LineAccounts, related_name='contacts', on_delete=models.CASCADE)
    contact_id      = models.CharField(max_length=50, db_index=True)
    contact_type    = models.CharField(choices=TYPE_CHOICES, max_length=16)
    nickname        = models.CharField(blank=True, max_length=50)
    display_name    = models.CharField(blank=True, max_length=255)
    created_on      = models.DateTimeField(auto_now_add=True)
    updated_on      = models.DateTimeField(auto_now=True)  # Also latest_message
    tag             = models.ManyToManyField('LineContactTag', blank=True, related_name='line_contacts')
    # last_message    = models.ForeignKey(LineContactMessage, blank=True, null=True, on_delete=models.SET_NULL)
    is_enabled      = models.BooleanField(default=True, db_index=True)  # ปิดก็ต่อเมื่อ บัญชีหายไปแล้วจากระบบ LINE

    # objects         = LineContactManager()

    
    def __str__(self):
        if self.nickname:
            return self.nickname
        elif self.display_name:
            return self.display_name
        else:
            return self.contact_id


class LineContactTag(models.Model):
    name         = models.CharField(max_length=255, unique=True, db_index=True)
    def __str__(self):
        return self.name


class TagGroup(models.Model):
    name        = models.CharField(max_length=255, unique=True, db_index=True)
    tag         = models.ManyToManyField('LineAccountTag', blank=True, related_name='groups')
    created_on  = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.name
