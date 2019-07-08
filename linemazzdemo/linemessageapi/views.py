from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.views import View
import hashlib 

from chatroom.models import ChatSession, ChatMessage

from linemessageapi.models import LineAccounts, LineContact

from linebot import LineBotApi, WebhookHandler

from linebot.exceptions import InvalidSignatureError

from linebot.models import MessageEvent

from datetime import datetime

class CallbackView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(slef, request, channel_id):
        line_account    = get_object_or_404(LineAccounts, active=True, channel_id=channel_id)
        line_bot_api    = LineBotApi(line_account.channel_access_token)
        handler         = WebhookHandler(line_account.channel_secret)

        signature   = request.META.get('HTTP_X_LINE_SIGNATURE', '')
        body        = request.body.decode('utf-8')

        @handler.add(MessageEvent)
        def handle_message(event):
            contact = line_account.getProfile(event.source)
            chat_session_list = ChatSession.objects.filter(line_account=line_account, line_contact=contact, end_conversation_at=None)
            if not chat_session_list :
                token = hashlib.md5("{}.{}".format(contact.contact_id, str(datetime.now())).encode('utf-8')).hexdigest()
                chat_session = ChatSession(
                    token               = token,
                    line_account        = line_account,
                    line_contact        = contact,
                )
                chat_session.save()
            else:
                chat_session = chat_session_list.first()

            text = ''
            file = None
            image = None

            if event.message.type == 'text':
                text = event.message.text
            
            # status coversation 
            # 0 คือ Contact คุยกับ Line@
            # 1 คือ Line@ คุยกับ Contact
            # ChatSession.objects.filter(line_account=line_account, line_contact=line_contact)
            
            chat_message = ChatMessage(
                session             = chat_session,
                line_account        = line_account,
                line_contact        = contact,
                message_type        = event.message.type,
                text                = text,
                image               = image,
                file                = file,
                raw_data            = body,
                status_coversation  = 0
            )
            chat_message.save()

        try:
            
            handler.handle(body, signature)

            # if not line_channel.is_verify_webhook:  # Verify webhook
            #     line_channel.is_verify_webhook = True
            #     line_channel.save()
        except InvalidSignatureError:
            return HttpResponseBadRequest('400 - Bad request')

        return HttpResponse('OK')
