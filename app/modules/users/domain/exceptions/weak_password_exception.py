from typing import Optional, Dict
from app.core.exceptions.base_exception import BaseApplicationError

class WeakPasswordException(BaseApplicationError):
    def __init__(
        self, 
        message: str = "Contraseña débil", 
        detail: Optional[Dict] = None 
    ):
        super().__init__(
            message=message,
            error_code="WEAK_PASSWORD",
            status_code=400,
            detail=detail
        )