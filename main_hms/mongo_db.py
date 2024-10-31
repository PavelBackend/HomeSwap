from motor.motor_asyncio import AsyncIOMotorClient
from main_hms import settings
from pymongo import MongoClient

MONGO_HOST = settings.MONGO_HOST
MONGO_PORT = settings.MONGO_PORT
MONGO_DB = settings.MONGO_DB
MONGO_INITDB_ROOT_USERNAME = settings.MONGO_INITDB_ROOT_USERNAME
MONGO_INITDB_ROOT_PASSWORD = settings.MONGO_INITDB_ROOT_PASSWORD

uri = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"

async_client = AsyncIOMotorClient(uri)

sync_client = MongoClient(uri)
