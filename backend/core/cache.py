# backend/core/cache.py

import os
import redis.asyncio as redis_lib

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis = redis_lib.from_url(REDIS_URL, decode_responses=True)

async def cache_get_verdict(seed: str, guess: str) -> str | None:
    key = f"{seed.lower()}::{guess.lower()}"
    return await redis.get(key)

async def cache_set_verdict(seed: str, guess: str, verdict: str):
    key = f"{seed.lower()}::{guess.lower()}"
    await redis.set(key, verdict, ex=3600)
