from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from .utils.logger import logger
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"Path: {request.url.path} Method: {request.method} "
            f"Processing Time: {process_time:.2f}s Status: {response.status_code}"
        )
        return response