# app/core/exception_handlers.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.core.response import ResponseModel
import logging

logger = logging.getLogger(__name__)

async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=ResponseModel(
            success=False,
            message="Ha ocurrido un error interno en el servidor",
            data=None,
            meta=None,
            error={
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "details": "Ha ocurrido un error inesperado. Intente más tarde."
            }
        ).dict()
    )

def register_core_exception_handlers(app: FastAPI):
    app.add_exception_handler(Exception, unhandled_exception_handler)