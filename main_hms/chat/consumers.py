import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from mongo_db import async_client
from main_hms import settings
import logging
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("Пользователь зашел в чат")
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        if await self.get_user_count() < 2:
            logger.info(
                f"Пользователь {self.scope['user'].username} встал в чат {self.room_name}"
            )
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.add_user()
            await self.accept()
        else:
            logger.info(
                f"Пользователь {self.scope['user'].username} не встал в чат {self.room_name}"
            )
            await self.close()

    async def disconnect(self, close_code):
        logger.info("Пользователь вышел из чата")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.remove_user()

    async def receive(self, text_data):
        logger.info("Получено сообщение")
        try:
            logger.info("Attempting to receive message...")
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", "")

            if message:
                logger.info("Attempting to save message...")
                await self.save_message(message)

                user = (
                    self.scope["user"].username
                    if self.scope["user"].is_authenticated
                    else "Anonymous"
                )

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "chat_message", "message": message, "user": user},
                )
        except Exception as e:
            logger.error(f"Error in receive method: {e}")
            await self.close(code=4000)

    async def save_message(self, message):
        logger.info("Attempting to save message in MongoDB...")
        try:
            db = async_client[settings.MONGO_DB]
            messages_collection = db["messages"]
            user = (
                self.scope["user"].username
                if self.scope["user"].is_authenticated
                else "Anonymous"
            )

            logger.info(
                f"Attempting to insert message in MongoDB for room {self.room_name} by user {user}"
            )

            await messages_collection.insert_one(
                {
                    "room": self.room_name,
                    "message": message,
                    "user": user,
                    "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
                }
            )

            from .tasks import send_notification_to_chat_to_email

            recipient_email = await self.post_author_email()
            if recipient_email:
                send_notification_to_chat_to_email.delay(
                    recipient_email, self.room_name
                )
        except Exception as e:
            logger.error(f"Error in save_message: {e}")
            await self.close(code=4000)

    def post_slug(self):
        logger.info("Attempting to get post slug...")
        try:
            return self.room_name.split("devisor")[1]
        except Exception as e:
            logger.error(f"Error in post_slug: {e}")
            raise

    @sync_to_async(thread_sensitive=True)
    def get_post_author_email_sync(self, post_slug):
        logger.info("Attempting to get post author email...")
        from posts.models import Posts

        post = get_object_or_404(Posts, slug=post_slug)
        return post.user.email

    async def post_author_email(self):
        logger.info("Attempting to get post author email...")
        try:
            post_slug = self.post_slug()
            email = await self.get_post_author_email_sync(post_slug)
            return email
        except Exception as e:
            logger.error(f"Error in post_author_email: {e}")
            await self.close(code=4000)

    async def chat_message(self, event):
        try:
            logger.info("Attempting to send message to WebSocket...")
            message = event["message"]
            user = event["user"]
            await self.send(text_data=json.dumps({"user": user, "message": message}))
        except Exception as e:
            logger.error(f"Error in chat_message: {e}")
            await self.close(code=4000)

    async def get_user_count(self):
        logger.info("Attempting to get user count...")
        db = async_client[settings.MONGO_DB]
        rooms_collection = db["rooms"]

        room = await rooms_collection.find_one({"room_name": self.room_name})
        return room["user_count"] if room else 0

    async def add_user(self):
        logger.info("Attempting to add user...")
        db = async_client[settings.MONGO_DB]
        rooms_collection = db["rooms"]

        await rooms_collection.update_one(
            {"room_name": self.room_name}, {"$inc": {"user_count": 1}}, upsert=True
        )

    async def remove_user(self):
        logger.info("Attempting to remove user...")
        db = async_client[settings.MONGO_DB]
        rooms_collection = db["rooms"]

        await rooms_collection.update_one(
            {"room_name": self.room_name}, {"$inc": {"user_count": -1}}
        )
