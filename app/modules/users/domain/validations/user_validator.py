from app.modules.users.domain.interfaces.user_repository import IUserRepository
from app.modules.users.domain.exceptions import WeakPasswordException, UserAlreadyExistsException
from app.modules.users.domain.models.models import UserCreateInput

class UserValidator:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def validate_user_create_input(self, user_input: UserCreateInput):
        await self._validate_email_unique(user_input.email)
        self._validate_password_strength(user_input.raw_password)

    async def _validate_email_unique(self, email: str):
        existing = await self.repo.find_by_email(email)
        if existing:
            raise UserAlreadyExistsException(email=email)

    def _validate_password_strength(self, password: str):
        if len(password) < 8:
            raise WeakPasswordException(detail={"reason": "La contraseña debe tener al menos 8 caracteres."})
        if not any(c.isupper() for c in password):
            raise WeakPasswordException(detail={"reason": "Debe contener al menos una letra mayúscula."})
        if not any(c.isdigit() for c in password):
            raise WeakPasswordException(detail={"reason": "Debe contener al menos un número."})
        if not any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for c in password):
            raise WeakPasswordException(detail={"reason": "Debe contener al menos un carácter especial."})