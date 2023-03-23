import logging
from threading import local
from typing import Any, Callable
import time

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)
_thread_locals = local()


class LoggingMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        _thread_locals.request = request
        self.process_request(request)
        response = self.get_response(request)
        response = self.process_response(request, response)
        return response

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        _thread_locals.total_time = time.time() - request.start_time
        return response

    def process_view(self, request: HttpRequest, view_func: Callable, *_: Any) -> None:
        _thread_locals.view = view_func


class RequestFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        request = getattr(_thread_locals, "request", PlaceHolder())
        total_time = getattr(_thread_locals, "total_time", PlaceHolder())
        print("1111111")
        print(type(total_time))
        if isinstance(total_time, float):
            record.total_time = f"{total_time:.2f} seconds"
        else:
            record.total_time = total_time
        record.request = request  # type: ignore
        record.remote_addr = self.get_remote_ip(request)  # type: ignore
        record.view = getattr(_thread_locals, "view", PlaceHolder())  # type: ignore
        record.user_id = request.user.id if request.user.is_authenticated else "-"  # type: ignore
        return super().format(record)

    @staticmethod
    def get_remote_ip(request: HttpRequest) -> str:
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded_for:
            return forwarded_for.split(",", 1)[0]
        return request.META.get("REMOTE_ADDR", PlaceHolder())


class PlaceHolder:
    def __init__(self, to_str: str = "-") -> None:
        self._to_str = to_str

    def __getattr__(self, name: str) -> "PlaceHolder":
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> "PlaceHolder":
        return self

    def __str__(self) -> str:
        return self._to_str

    def __repr__(self) -> str:
        return self._to_str

    def __bool__(self) -> bool:
        return False
