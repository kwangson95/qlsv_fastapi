from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.core.common import exceptions as ex


async def exception_handler(_: Request, exc: ex.GenericError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_code": exc.code or 999,
            "message": exc.message or "unknown error",
        },
    )
