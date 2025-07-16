from typing import Type, Callable, Dict, List
from app.core.events.base import DomainEvent

class EventBus:
    def __init__(self):
        self._subscribers: Dict[Type[DomainEvent], List[Callable]] = {}

    def subscribe(self, event_type: Type[DomainEvent], handler: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, event: DomainEvent):
        handlers = self._subscribers.get(type(event), [])
        for handler in handlers:
            await handler(event)

event_bus = EventBus()
