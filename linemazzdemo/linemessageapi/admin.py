from django.contrib import admin

# Register your models here.
from .models import LineAccountTag, LineAccounts, LineContact, LineContactTag, TagGroup


@admin.register(LineAccountTag)
class LineAccountTagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'priority')
    search_fields   = ['name']


@admin.register(LineAccounts)
class LineAccountsAdmin(admin.ModelAdmin):
    list_filter     = ['nickname', 'channel_id']
    search_fields   = ['nickname']


@admin.register(LineContact)
class LineContactAdmin(admin.ModelAdmin):
    list_display    = ('id', 'display_name', 'contact_type', 'channel')
    list_filter     = ['channel']
    search_fields   = ['nickname']


@admin.register(LineContactTag)
class LineContactTagAdmin(admin.ModelAdmin):
    pass

@admin.register(TagGroup)
class TagGroupMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_tags')

    def get_tags(self, obj):
        result = ''
        if obj.tag.exists():
            result =  ', '.join(list(obj.tag.order_by('name').values_list('name', flat=True)))
        
        return result