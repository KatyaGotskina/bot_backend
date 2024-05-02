from functools import wraps
from typing import Callable, Union

from starlette import status
from fastapi.responses import JSONResponse

from backend.utils.exceptions import NotFoundException, IncorrectDataException


def create_error_response(error: Union[Exception, str], status_code: int = status.HTTP_400_BAD_REQUEST) -> JSONResponse:
    return JSONResponse({"error": str(error)}, status=status_code)


def handle_domain_exceptions(func: Callable) -> Callable:
    """Декоратор для обработки DomainException."""

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except NotFoundException as e:
            return create_error_response(e, status_code=status.HTTP_404_NOT_FOUND)
        except IncorrectDataException as e:
            return create_error_response(e)
    return wrapper