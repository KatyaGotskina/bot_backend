from fastapi import Depends, Request
from starlette import status
from starlette.responses import Response

from backend.core.postgres import DBWork
from backend.core.postgres_engine import get_db_work
from backend.endpoints.routers import user_router
from backend.models.models import User
from backend.schemas.user import TimezoneOffset
from backend.utils.decorators import handle_domain_exceptions


@handle_domain_exceptions
@user_router.post('')
async def change_timezone(
    request: Request,
    body: TimezoneOffset,
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    user_id = int(request.headers.get('user_from_id'))
    if not await db_work.get_obj(model=User, where={'id': user_id}):
        await db_work.create_obj(User, data_for_create={'id': user_id})
    await db_work.update_obj(model=User, where={'id': user_id}, for_set={'timezone_offset': body.offset})
    return Response(status_code=status.HTTP_200_OK)
