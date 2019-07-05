from django.db import models

from django.contrib.auth.models import AbstractUser

from linemessageapi.models import TagGroup, LineAccountTag

# class User(AbstractUser):
#     tag_group           = models.ForeignKey(TagGroup, blank=True, null=True, on_delete=models.SET_NULL)
#     permission_tags     = models.ManyToManyField(LineAccountTag, blank=True, null=True)