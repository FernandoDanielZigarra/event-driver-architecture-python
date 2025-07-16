from app.modules.users.domain.events.events import UserCreatedEvent

async def send_welcome_email(event: UserCreatedEvent):
    print(f"📨 Email de bienvenida enviado a: {event.email} (ID: {event.id})")
