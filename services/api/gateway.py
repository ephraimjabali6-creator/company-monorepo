import os
import time
from typing import Dict, Tuple

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

# Rate limiter: prefer Redis if REDIS_URL is configured; otherwise fall back to in-memory.
_RATE_TABLE: Dict[str, Tuple[int, float]] = {}
_RATE_LIMIT = int(os.getenv("GATEWAY_RATE_LIMIT", "5"))
_RATE_WINDOW = int(os.getenv("GATEWAY_RATE_WINDOW", "10"))  # seconds

# Redis client is optional; lazily imported and created if REDIS_URL exists
_redis_client = None


def _get_redis():
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        return None
    # support a testing fake redis via URL scheme faker://
    if redis_url.startswith("faker://"):
        try:
            import fakeredis
            _redis_client = fakeredis.FakeRedis()
            return _redis_client
        except Exception:
            return None
    try:
        import redis
        _redis_client = redis.from_url(redis_url, decode_responses=True)
        return _redis_client
    except Exception:
        # Redis not available — fall back to in-memory
        return None


def _valid_api_key(key: str) -> bool:
    keys = os.getenv("API_KEYS", "").split(",") if os.getenv("API_KEYS") else []
    keys = [k.strip() for k in keys if k and k.strip()]
    return key in keys


def _check_rate_redis(key: str):
    r = _get_redis()
    if not r:
        raise RuntimeError("redis-not-available")
    # Use INCR with EXPIRE to implement sliding window approximate limiter
    bucket = f"rate:{key}"
    count = r.incr(bucket)
    if r.ttl(bucket) == -1:
        r.expire(bucket, _RATE_WINDOW)
    if int(count) > _RATE_LIMIT:
        raise RuntimeError("rate-limit-exceeded")


def _check_rate_inmemory(key: str):
    now = time.time()
    count, window_start = _RATE_TABLE.get(key, (0, now))
    if now - window_start > _RATE_WINDOW:
        # reset window
        count, window_start = (0, now)
    count += 1
    _RATE_TABLE[key] = (count, window_start)
    if count > _RATE_LIMIT:
        raise RuntimeError("rate-limit-exceeded")


def _check_rate(key: str):
    # try redis first
    r = _get_redis()
    if r:
        _check_rate_redis(key)
        return
    _check_rate_inmemory(key)


async def api_key_and_rate_middleware(request: Request, call_next):
    # Enforce API key + rate limiting only for gateway-prefixed paths.
    path = request.url.path
    if not path.startswith("/gateway"):
        return await call_next(request)

    # Allow health probes under gateway without key
    if path.startswith("/gateway/health") or path == "/gateway/health":
        return await call_next(request)

    api_key = request.headers.get("x-api-key") or request.headers.get("X-API-KEY")
    if not api_key:
        return JSONResponse(status_code=401, content={"detail": "missing API key"})

    if not _valid_api_key(api_key):
        return JSONResponse(status_code=403, content={"detail": "invalid API key"})

    try:
        _check_rate(api_key)
    except RuntimeError as e:
        msg = str(e)
        if "rate-limit" in msg:
            return JSONResponse(status_code=429, content={"detail": "rate limit exceeded"})
        # redis not available — fall back to in-memory check
        try:
            _check_rate_inmemory(api_key)
        except RuntimeError:
            return JSONResponse(status_code=429, content={"detail": "rate limit exceeded"})

    return await call_next(request)


def attach_middleware(app):
    # registers the middleware on the FastAPI app instance
    app.middleware("http")(api_key_and_rate_middleware)


@router.get("/echo")
async def echo():
    return {"ok": True, "message": "gateway OK"}
