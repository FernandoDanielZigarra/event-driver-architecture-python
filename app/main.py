from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.db.db import db
from app.modules.users.api.routes import router as users_router
from typing import AsyncGenerator
from pathlib import Path
from importlib import import_module
from app.core.exception_handlers import register_core_exception_handlers
from app.core.events.loader import register_all_subscriptions
from app.core.response import ResponseModel
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await db.connect()
    print("✅ Base de datos conectada")

    register_all_subscriptions()

    yield

    await db.disconnect()
    print("🛑 Base de datos desconectada")

app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    simplified_errors = [
        {"loc": err["loc"], "msg": err["msg"], "type": err["type"]}
        for err in errors
    ]
    return JSONResponse(
        status_code=422,
        content=ResponseModel(
            success=False,
            message="Error de validación en la solicitud",
            data=None,
            meta=None,
            error=simplified_errors
        ).dict()
    )


def register_module_exception_handlers(app: FastAPI):
    base_path = Path(__file__).parent / "modules"
    for module in base_path.iterdir():
        exception_path = module / "exception_handlers.py"
        if exception_path.exists():
            mod_path = f"app.modules.{module.name}.exception_handlers"
            handlers_module = import_module(mod_path)
            if hasattr(handlers_module, "get_exception_handlers"):
                exception_handlers = handlers_module.get_exception_handlers()
                for exc_class, handler in exception_handlers.items():
                    app.add_exception_handler(exc_class, handler)


register_module_exception_handlers(app)
register_core_exception_handlers(app)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel(
            success=False,
            message=exc.detail if isinstance(
                exc.detail, str) else "Error HTTP",
            data=None,
            meta=None,
            error={"code": exc.status_code, "details": exc.detail}
        ).dict()
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ResponseModel(
            success=False,
            message="Ha ocurrido un error interno en el servidor",
            data=None,
            meta=None,
            error={"code": 500, "details": str(exc)}
        ).dict()
    )


app.include_router(users_router, prefix="/api/v1", tags=["Users"])
