from src.database.abc import ViewRepository

from .models import ClientORM, WorkPlaceORM
from ..database.repos import ClientColumnRepository, WorkPlaceColumnRepository


class ClientsRepository(ViewRepository):
    orm_model = ClientORM
    columns_repository = ClientColumnRepository


class WorkPlaceRepository(ViewRepository):
    orm_model = WorkPlaceORM
    columns_repository = WorkPlaceColumnRepository
    