from fastapi import Request, status
from fastapi.responses import JSONResponse

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if not request.headers.get('user_from_id') and str(request.url).split('/')[-1] not in ['openapi.json ', 'swagger', 'metrics']:
            return JSONResponse(content={'err': "No auth header"}, status_code=status.HTTP_401_UNAUTHORIZED)
        response = await call_next(request)
        return response
