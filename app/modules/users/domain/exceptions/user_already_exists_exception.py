from typing import Optional, Dict
from app.core.exceptions.base_exception import BaseApplicationError


class UserAlreadyExistsException(BaseApplicationError):
    def __init__(
        self,
        email: str,
        detail: Optional[Dict] = None
    ):
        super().__init__(
            message=f"El usuario con email '{email}' ya existe.",
            error_code="USER_ALREADY_EXISTS",
            status_code=409,
            detail=detail or {"email": email}
        )
