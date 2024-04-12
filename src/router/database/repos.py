from sqlalchemy import Select, select

from src.database import Repository

from .models import ClientColumnORM, ProfessionColumnORM, WorkPlaceColumnORM


class ClientColumnRepository(Repository):
    orm_model = ClientColumnORM


class WorkPlaceColumnRepository(Repository):
    orm_model = WorkPlaceColumnORM


class ProfessionColumnRepository(Repository):
    orm_model = ProfessionColumnORM
