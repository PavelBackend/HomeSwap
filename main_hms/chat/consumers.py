import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from mongo_db import async_client
from main_hms import settings


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        if await self.get_user_count() < 2:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.add_user()
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.remove_user()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        if message:
            await self.save_message(message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    async def save_message(self, message):
        db = async_client[settings.MONGO_DB]
        messages_collection = db['messages']
        user = self.scope['user'].username if self.scope['user'].is_authenticated else 'Anonymous'

        await messages_collection.insert_one({
            'room': self.room_name,
            'message': message,
            'user': user,
            'timestamp': datetime.datetime.now(tz=datetime.timezone.utc)
        })

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def get_user_count(self):
        db = async_client[settings.MONGO_DB]
        rooms_collection = db['rooms']
        
        room = await rooms_collection.find_one({'room_name': self.room_name})
        return room['user_count'] if room else 0

    async def add_user(self):
        db = async_client[settings.MONGO_DB]
        rooms_collection = db['rooms']
        
        await rooms_collection.update_one(
            {'room_name': self.room_name},
            {'$inc': {'user_count': 1}},
            upsert=True
        )

    async def remove_user(self):
        db = async_client[settings.MONGO_DB]
        rooms_collection = db['rooms']
        
        await rooms_collection.update_one(
            {'room_name': self.room_name},
            {'$inc': {'user_count': -1}}
        )
