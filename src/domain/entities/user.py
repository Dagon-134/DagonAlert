from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    
    tg_id: str
    name: str
    created_at: datetime
    source: str
    
    