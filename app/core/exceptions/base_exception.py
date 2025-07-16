from typing import Optional, Dict

class BaseApplicationError(Exception):
    def __init__(
        self,
        message: str = "Error desconocido",
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        detail: Optional[Dict] = None, 
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(message)