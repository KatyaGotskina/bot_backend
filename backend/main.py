from fastapi import FastAPI
import uvicorn
from backend.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

from backend.endpoints.routers import task_router


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def setup_routers(app: FastAPI) -> None:
    app.include_router(task_router)


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger')
    setup_routers(app)

    setup_middleware(app)

    return app


if __name__ == '__main__':
    uvicorn.run('main:create_app', host='0.0.0.0', port=8000, factory=True, reload=True)
