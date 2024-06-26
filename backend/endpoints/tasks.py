import datetime
from typing import Optional
from uuid import UUID

from fastapi import Depends, Query, Request
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.responses import Response

from backend.endpoints.routers import task_router
from backend.core.postgres_engine import get_db_work
from backend.core.postgres import DBWork
from backend.models.task import Task
from backend.models.task_category import TaskCategory
from backend.models.user import User
from backend.schemas.task import TaskCreate, TaskModel

from backend.schemas.task import TaskNameUpdate, TaskToCategory
from backend.schemas.useful import Id
from backend.utils.decorators import handle_domain_exceptions


@task_router.get('/all', response_model=list[TaskModel])
async def get_tasks(
    request: Request,
    undone: Optional[bool] = Query(default=False, description='поиск незавершенных дел'),
    category: Optional[UUID] = Query(default=None, description='поиск дел по категории'),
    limit: Optional[int] = Query(default=5),
    offset: Optional[int] = Query(default=0),
    db_work: DBWork = Depends(get_db_work)
) -> ORJSONResponse:
    user_id = int(request.headers.get('user_from_id'))
    if not await db_work.get_obj(model=User, where={'id': user_id}):
        return ORJSONResponse([])
    filter_dict = {'user_id': user_id}
    if undone:
        filter_dict['end'] = None
    if category:
        filter_dict['categories'] = [category]
    tasks = await db_work.get_obj(
        model=Task,
        where=filter_dict,
        field_for_load='categories',
        field_for_order='start',
        limit=limit,
        offset=offset
    )
    return ORJSONResponse([TaskModel.model_validate(task).model_dump(mode='json') for task in tasks])


@task_router.post('')
async def create_task(
    request: Request,
    body: TaskCreate,
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    user_id = int(request.headers.get('user_from_id'))
    user = await db_work.get_obj(model=User, where={'id': user_id})
    if not user:
        user = await db_work.create_obj(User, data_for_create={'id': user_id})
    else:
        user = user[0]
        if not user.chat_id:
            await db_work.update_obj(
                User,
                where={'id': user_id},
                for_set={'chat_id': int(request.headers.get('user_chat_id'))}
            )
    if await db_work.get_obj(model=Task, where={'name': body.name}) and not body.forcibly:
        return Response(status_code=status.HTTP_409_CONFLICT)
    tz = datetime.timezone(datetime.timedelta(hours=user.timezone_offset))
    task = await db_work.create_obj(
        Task,
        {
            'name': body.name,
            'user_id': user_id,
            'start': datetime.datetime.now(tz=tz),
            'timezone_offset': user.timezone_offset
        }
    )
    return ORJSONResponse({'id': task.id}, status_code=status.HTTP_201_CREATED)


@task_router.delete('/{task_id}')
async def delete_task(
    request: Request,
    task_id: int,
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    task = await db_work.get_obj(Task, where={'id': task_id, 'user_id': int(request.headers.get('user_from_id'))})
    if not task:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await db_work.delete_obj(Task, {'id': task_id})
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@task_router.patch('/name')
@handle_domain_exceptions
async def change_task_name(
    body: TaskNameUpdate,
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    if await db_work.get_obj(model=Task, where={'name': body.name}) and not body.forcibly:
        return Response(status_code=status.HTTP_409_CONFLICT)
    await db_work.update_obj(Task, where={'id': body.id}, for_set={'name': body.name})
    return Response(status_code=status.HTTP_200_OK)


@task_router.patch('/end')
@handle_domain_exceptions
async def change_task_end(
    request: Request,
    body: Id,
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    task = await db_work.get_obj(Task, where={'id': body.id, 'user_id': int(request.headers.get('user_from_id'))})
    if not task:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await db_work.update_obj(Task, where={'id': body.id, 'end': None}, for_set={'end': datetime.now()})
    return Response(status_code=status.HTTP_200_OK)


@task_router.put('/match_to_category')
async def match_task_to_category(
    body: TaskToCategory,
    db_work: DBWork = Depends(get_db_work),
) -> Response:

    await db_work.create_obj(TaskCategory, data_for_create={'category_id': body.category_id, 'task_id': body.task_id})
    return Response(status_code=status.HTTP_200_OK)
