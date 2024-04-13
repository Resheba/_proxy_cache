from src.database.abc import ViewRepository

from .models import ClientORM, WorkPlaceORM, ProfessionORM
from ..database.repos import ClientColumnRepository, WorkPlaceColumnRepository, ProfessionColumnRepository


class ClientsRepository(ViewRepository):
    orm_model = ClientORM
    columns_repository = ClientColumnRepository


class WorkPlaceRepository(ViewRepository):
    orm_model = WorkPlaceORM
    columns_repository = WorkPlaceColumnRepository


class ProfessionsRepository(ViewRepository):
    orm_model = ProfessionORM 
    columns_repository = ProfessionColumnRepository
    