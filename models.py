from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEntry:
    time: datetime
    method: str
    path: str
    status_code: int
    latency_ms: int
    user: str
    model: str

class ParseError(Exception):
    pass

class ConfigError(Exception):
    pass