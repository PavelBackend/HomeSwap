from django.shortcuts import render
from django.views import View
from mongo_db import sync_client
from main_hms import settings

class ChatView(View):
    def get(self, request, room_name):
        db = sync_client[settings.MONGO_DB]
        messages_collection = db['messages']
        
        messages = messages_collection.find({'room': room_name}).sort('timestamp')
        
        message_list = [{'message': msg['message']} for msg in messages]
        context = {'room_name': room_name, 'messages': message_list}
        
        return render(request, 'chat/chat.html', context)
