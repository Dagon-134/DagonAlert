from dataclasses import dataclass
from src.domain.value_objects.subscription_level import SubscriptionLevel
from src.domain.entities.user import User
from datetime import datetime

@dataclass
class Subscription:
    
    id: str
    level: SubscriptionLevel
    user: User
    created_at: datetime
    expires_at: datetime
    