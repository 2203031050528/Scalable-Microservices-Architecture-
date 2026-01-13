import os
from dotenv import load_dotenv
import redis.asyncio as redis
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

async def get_redis():
    return redis.from_url(REDIS_URL, decode_responses=True)