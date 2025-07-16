from app.core.events.event_bus import event_bus
from app.modules.users.domain.events.events import UserCreatedEvent
from app.modules.users.application.handlers.handlers import send_welcome_email

def subscribe_user_events():
    event_bus.subscribe(UserCreatedEvent, send_welcome_email)
