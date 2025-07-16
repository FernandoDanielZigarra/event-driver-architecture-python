from typing import Generic, TypeVar, Optional,Any
from pydantic import BaseModel, ConfigDict
from fastapi.responses import JSONResponse

T = TypeVar("T")  # Tipo para `data`
M = TypeVar("M")  # Tipo para `meta`
E = TypeVar("E")  # Tipo para `error`

class ResponseModel(BaseModel, Generic[T, M, E]):
    success: bool
    message: str
    data: Optional[T] = None
    meta: Optional[M] = None
    error: Optional[E] = None

    model_config = ConfigDict(extra="forbid", frozen=True)

def success_response(
    message: str,
    data: Optional[T] = None,
    meta: Optional[M] = None
) -> ResponseModel[T, M, None]:
    return ResponseModel(success=True, message=message, data=data, meta=meta, error=None)


def error_response(
    message: str,
    error: Any,
    data: Optional[Any] = None,
    meta: Optional[Any] = None,
    status_code: int = 400,
) -> JSONResponse:
    payload = ResponseModel(
        success=False,
        message=message,
        data=data,
        meta=meta,
        error=error
    )
    return JSONResponse(
        content=payload.model_dump(),
        status_code=status_code
    )