from collections import deque
from datetime import datetime
from typing import List, Dict, Any

_LOG_BUFFER: deque = deque(maxlen=500)


def log(team: str, message: str, level: str = "info"):
    _LOG_BUFFER.appendleft({
        "ts": datetime.utcnow().isoformat() + "Z",
        "team": team,
        "level": level,
        "message": message,
    })


def recent(n: int = 50) -> List[Dict[str, Any]]:
    return list(_LOG_BUFFER)[:n]
