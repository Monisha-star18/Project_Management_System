from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.base_exception import AppException
from app.utilites.logger import logger


async def app_exception_handler( request: Request, exc: AppException ):

    logger.warning(
        "Application error | Path=%s | Error=%s",
        request.url.path,
        exc.message
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message
        }
    )
