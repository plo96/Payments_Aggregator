from dataclasses import dataclass
from datetime import datetime


@dataclass
class Payment:
    _id: str
    value: int
    dt: datetime
