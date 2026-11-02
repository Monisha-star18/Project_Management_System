import time 
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utilites.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):

    #The dispatch() method runs automatically whenever an HTTP request passes through this middleware.
    async def dispatch(self, request:Request, call_next):

        start_time = time.perf_counter() #useful for measuring elapsed time because it uses a monotonic performance clock.

        try:
            response = await call_next(request)

            duration = (time.perf_counter() - start_time) * 1000
            
            logger.info(
                "Method=%s | Path=%s | Status=%s | Duration=%.2fms",
                request.method,
                request.url.path,
                response.status_code,
                duration
            )

            return response

        except Exception as er  :
            logger.exception(
                "Unhandled error| Method=%s | Path=%s | Error=%s ",
                request.method,
                request.url.path,
                er
            )

            raise

