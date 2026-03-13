"""
Shared MongoDB connection helper — reference implementation.
Each service includes its own database.py with its specific document models.
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

load_dotenv()

MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME: str = os.getenv("DATABASE_NAME", "ai_recruitment")

_client: AsyncIOMotorClient = None


async def connect_db(document_models: list) -> None:
    """Call at app startup. Pass all Beanie Document classes for the service."""
    global _client
    _client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=_client[DATABASE_NAME], document_models=document_models)
    print(f"Connected to MongoDB — database: {DATABASE_NAME}")


async def close_db() -> None:
    global _client
    if _client:
        _client.close()
        print("Disconnected from MongoDB")
