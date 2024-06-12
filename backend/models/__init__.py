from sqlalchemy.orm import configure_mappers

from . import category
from . import task
from . import task_category
from . import user

configure_mappers()
