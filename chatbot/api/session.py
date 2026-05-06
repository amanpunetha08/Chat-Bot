import json
import uuid
from datetime import datetime

import redis
from django.conf import settings


_redis = redis.from_url(settings.REDIS_URL, decode_responses=True)


def create_session():
    return str(uuid.uuid4())


def add_message(session_id, role, content):
    entry = {"role": role, "content": content, "timestamp": datetime.utcnow().isoformat()}
    _redis.rpush(f"chat:{session_id}", json.dumps(entry))
    _redis.expire(f"chat:{session_id}", 86400)  # 24h TTL


def get_history(session_id):
    raw = _redis.lrange(f"chat:{session_id}", 0, -1)
    return [json.loads(m) for m in raw]


def clear_session(session_id):
    return _redis.delete(f"chat:{session_id}")
