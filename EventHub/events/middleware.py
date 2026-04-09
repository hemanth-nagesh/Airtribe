import logging
import time

from django.utils import timezone

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("RequestLoggingMiddleware initialized")

    def __call__(self, request):
        start_time = timezone.now()
        start_counter = time.perf_counter()
        logger.info(
            "Before view: %s %s | start_time=%s",
            request.method,
            request.path,
            start_time.isoformat(),
        )
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start_counter) * 1000
        logger.info(
            "After view: %s %s -> %s | start_time=%s | duration_ms=%.2f",
            request.method,
            request.path,
            response.status_code,
            start_time.isoformat(),
            duration_ms,
        )
        return response
