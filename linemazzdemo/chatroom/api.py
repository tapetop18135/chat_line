from django.http import JsonResponse
from .models import ChatMessage, ChatSession
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

import requests

def result_message_list(message_list):
    message_result_list = []
    for message in message_list:
        message_ = ""
        name_display = ""
        if(message.message_type=="text"):
            message_ = message.text
        elif(message.message_type=="img"):
            message_ = message.image
        elif(message.message_type=="file"):
            message_ = message.file

        if message.status_coversation == '0':
            name_display = message.line_contact.display_name
        else:
            name_display = message.line_account.nickname
            
        temp_message = [{
            "display_name" : name_display,
            "message" : message_,
            "date_message" : message.created_on.strftime('%Y/%m/%d %H:%M:%S:%f'),
            "status_conver" : message.status_coversation,
            "message_type" : message.message_type
        }]

        message_result_list = temp_message + message_result_list

    return message_result_list

def get_session(session):
    session_list = ChatSession.objects.filter(token=session)
    if not session_list:
        return JsonResponse({"error":"no session in db"})
    session_list = session_list.filter(end_conversation_at=None)
    if not session_list:
        return JsonResponse({"error":"session has expire"})
    session_now = session_list.first()
    return session_now

def get_message(request):
    import pytz; utc=pytz.UTC
    session = request.GET.get("token")
    session_now = get_session(session)
    
    limit_message = 10
    mode_get_message = request.GET.get('mode_get_message')
    if mode_get_message == 'update' :
        time_last = request.GET.get('time_last')
        time_last = datetime.strptime(time_last, '%Y/%m/%d %H:%M:%S:%f')     
         
        message_list = ChatMessage.objects.filter(session=session_now).order_by("-created_on").filter(created_on__gt = utc.localize(time_last))
        message_result_list = result_message_list(message_list)
    else:
        message_list = ChatMessage.objects.filter(session=session_now).order_by("-created_on")[:limit_message]
        message_result_list = result_message_list(message_list)
    
    return JsonResponse({"data": message_result_list})

def get_lazy_message(request):

    session = request.GET.get("token")
    session_now = get_session(session)
    limit_lazy_message = 10
    start_message = int(request.GET.get('start_message'))
    end_message = start_message + limit_lazy_message 
    message_list = ChatMessage.objects.filter(session=session_now).order_by("-created_on")[start_message:end_message]
    message_result_list = result_message_list(message_list)

    return JsonResponse({"data": message_result_list})
    
@csrf_exempt
def send_message(request):
    import json
    if request.method == "POST":
        session = request.GET.get("token")
        session_now = get_session(session)
        text = ""
        image = None
        file = None
        message_dict = json.loads(request.body)

        message_type = message_dict["message_type"]
        message = message_dict["message"]

        if(message_type == "text"):
            text = message
        
        elif(message_type == "image"):
            image = message
        
        elif(message_type == "file"):
            file = message
        try:
            chat_message = ChatMessage(
                    session             = session_now,
                    line_account        = session_now.line_account,
                    line_contact        = session_now.line_contact,
                    message_type        = message_type,
                    text                = text,
                    image               = image,
                    file                = file,
                    raw_data            = str(message_dict),
                    status_coversation  = 1
                )
                
            chat_message.save()
            try:
                data = {
                    "to": session_now.line_contact.contact_id,
                    "messages":[
                        {
                            "type": chat_message.message_type,
                            "text": chat_message.text
                        }
                    ]
                }

                headers = {
                    "Content-Type" : "application/json",
                    "Authorization" : "Bearer {}".format(session_now.line_account.channel_access_token)
                }
                
                headers = {
                    'Authorization': 'Bearer {}'.format(session_now.line_account.channel_access_token), 
                    'Content-type': 'application/json',
                }
                response = requests.post('https://api.line.me/v2/bot/message/push', data=json.dumps(data), headers=headers)
                if(response.status_code == 200):
                    return JsonResponse({"data": "ส่งได้แล้ว"})
                return JsonResponse({"error": "ไม่สามารถส่ง line ได้แต่เก็บลง database แล้ว"})
            except:
                return JsonResponse({"error": "ไม่สามารถส่ง line ได้แต่เก็บลง database แล้ว"})
        except:
            return JsonResponse({"error": "ไม่สามารถเก็บลง database ได้"})
    
    