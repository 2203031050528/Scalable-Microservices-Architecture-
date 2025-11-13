import aioredis
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

redis = None

async def get_redis():
    global redis
    if redis is None:
        redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
    return redis
