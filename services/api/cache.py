"""Optional cache/session helpers for Redis (fallbacks included).
"""
import os
from typing import Any, Optional


class RedisCache:
    def __init__(self, client=None):
        self.client = client

    @classmethod
    def from_env(cls):
        url = os.getenv('REDIS_URL')
        if url and url.startswith('faker://'):
            import fakeredis
            return cls(fakeredis.FakeRedis())
        if url:
            import redis
            return cls(redis.from_url(url, decode_responses=True))
        return cls(None)

    def get(self, key: str) -> Optional[str]:
        if not self.client:
            return None
        return self.client.get(key)

    def set(self, key: str, value: Any, ex: int = None):
        if not self.client:
            return None
        return self.client.set(key, value, ex=ex)


class SessionManager:
    def __init__(self, cache: RedisCache):
        self.cache = cache

    def create_session(self, user_id: str) -> str:
        import secrets
        sid = secrets.token_urlsafe(24)
        self.cache.set(f"sess:{sid}", user_id, ex=3600)
        return sid

    def get_user(self, sid: str) -> Optional[str]:
        return self.cache.get(f"sess:{sid}")
