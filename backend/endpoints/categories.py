from fastapi import Depends, Query
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.responses import Response

from backend.endpoints.routers import category_router
from backend.core.postgres_engine import get_db_work
from backend.models.models import Category
from backend.core.postgres import DBWork
from backend.schemas.category import CategoryModel

from backend.schemas.category import CategoryCreate
from backend.schemas.useful import Id
from backend.utils.decorators import handle_domain_exceptions


@category_router.get('/all', response_model=list[CategoryModel])
async def get_categories(
    db_work: DBWork = Depends(get_db_work)
) -> ORJSONResponse:
    categories = await db_work.get_obj(model=Category)
    return ORJSONResponse([CategoryModel(elem) for elem in categories])


@category_router.post('')
async def create_category(
    body: CategoryCreate,
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    if await db_work.get_obj(model=Category, where={'name': body.name}):
        return Response(status_code=status.HTTP_409_CONFLICT)
    category = await db_work.create_obj(Category, {'name': body.name})
    return ORJSONResponse({'id': category.id}, status_code=status.HTTP_201_CREATED)


@category_router.patch('/name')
@handle_domain_exceptions
async def change_category_name(
    body: CategoryModel,
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    if await db_work.get_obj(model=Category, where={'name': body.name}):
        return Response(status_code=status.HTTP_409_CONFLICT)
    await db_work.update_obj(Category, where={'id': body.id}, for_set={'name': body.name})
    return Response(status_code=status.HTTP_200_OK)


@category_router.delete('')
async def delete_category(
    category_id: Id,
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    await db_work.delete_obj(Category, {'id': category_id})
    return Response(status_code=status.HTTP_204_NO_CONTENT)
