from config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.Schedule import Schedule
from models.Trip import Trip

settings = get_settings()

async def init_db():
    client = AsyncIOMotorClient(settings.mongodb_uri)
    await init_beanie(
        database=client[settings.mongodb_database],
        document_models=[Trip, Schedule],)