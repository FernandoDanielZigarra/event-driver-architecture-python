from dataclasses import dataclass
from app.core.events.base import DomainEvent
from uuid import UUID

@dataclass
class UserCreatedEvent(DomainEvent):
    id: UUID
    email: str
