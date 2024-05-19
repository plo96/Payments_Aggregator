from dataclasses import dataclass
from datetime import datetime


@dataclass
class Payment:
    """Схема платежей."""
    _id: str
    value: int
    dt: datetime
