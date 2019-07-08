from django.core.management.base import BaseCommand, CommandError
from chatroom.models import ChatMessage, ChatSession

import time
import datetime
import pytz; utc=pytz.UTC

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print('xxxx')
        # while(True):
        session_list = ChatSession.objects.filter(end_conversation_at = None)
        for session in session_list:
            chat_now = ChatMessage.objects.filter(session=session).order_by("-created_on").first()
            delta_time = utc.localize(datetime.datetime.now()) - chat_now.created_on
            
            print(delta_time)
            import pdb; pdb.set_trace()
                

            # time.sleep(5)
