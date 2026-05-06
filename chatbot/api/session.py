import json
import uuid
from datetime import datetime

from django.conf import settings

_memory_store = {}

try:
    import redis
    _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    _redis.ping()
    USE_REDIS = True
except Exception:
    USE_REDIS = False


def create_session():
    return str(uuid.uuid4())


def add_message(session_id, role, content):
    entry = {"role": role, "content": content, "timestamp": datetime.utcnow().isoformat()}
    if USE_REDIS:
        _redis.rpush(f"chat:{session_id}", json.dumps(entry))
        _redis.expire(f"chat:{session_id}", 86400)
    else:
        _memory_store.setdefault(session_id, []).append(entry)


def get_history(session_id):
    if USE_REDIS:
        raw = _redis.lrange(f"chat:{session_id}", 0, -1)
        return [json.loads(m) for m in raw]
    return _memory_store.get(session_id, [])


def clear_session(session_id):
    if USE_REDIS:
        return _redis.delete(f"chat:{session_id}")
    _memory_store.pop(session_id, None)
