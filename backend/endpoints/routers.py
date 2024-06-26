from fastapi import APIRouter

task_router = APIRouter(prefix='/api/task')
category_router = APIRouter(prefix='/api/category')
user_router = APIRouter(prefix='/api/user')
