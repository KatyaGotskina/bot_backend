from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from starlette import status
from starlette.responses import Response

from backend.endpoints.routers import task_router
from backend.core.postgres_engine import get_session, get_db_work
from backend.models.models import Task
from backend.core.postgres import DBWork
from backend.schemas.task import TaskCreate, TaskModel

from backend.models.models import TaskCategory
from backend.schemas.task import TaskNameUpdate, TaskToCategory
from backend.schemas.useful import Id
from backend.utils.decorators import handle_domain_exceptions


@task_router.get('/all', response_model=list[TaskModel])
async def get_tasks(
    undone: Optional[bool] = Query(default=False, description='поиск незавершенных дел'),
    category: Optional[UUID] = Query(default=None, description='поиск дел по категории'),
    db_work: DBWork = Depends(get_db_work)
) -> JSONResponse:
    filter_dict = {}
    if undone:
        filter_dict['end'] = None
    if category:
        filter_dict['categories'] = [category]
    tasks = await db_work.get_obj(model=Task, where=filter_dict, field_for_load='categories')
    return JSONResponse([TaskModel.model_validate(task).model_dump(mode='json') for task in tasks])


@task_router.post('')
async def create_task(
    body: TaskCreate,
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    if await db_work.get_obj(model=Task, where={'name': body.name}) and not body.forcibly:
        return Response(status_code=status.HTTP_409_CONFLICT)
    task = await db_work.create_obj(Task, {'name': body.name})
    return JSONResponse({'id': task.id}, status_code=status.HTTP_201_CREATED)


@task_router.delete('')
async def delete_task(
    task_id: Id,
    db_work: DBWork = Depends(get_db_work),
) -> Response:
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
    body: Id,
    db_work: DBWork = Depends(get_db_work),
) -> Response:

    await db_work.update_obj(Task, where={'id': body.id, 'end': None}, for_set={'end': datetime.now()})
    return Response(status_code=status.HTTP_200_OK)


@task_router.put('/match_to_category')
async def match_task_to_category(
    body: TaskToCategory,
    db_work: DBWork = Depends(get_db_work),
) -> Response:

    await db_work.create_obj(TaskCategory, data_for_create={'category_id': body.category_id, 'task_id': body.task_id})
    return Response(status_code=status.HTTP_200_OK)
