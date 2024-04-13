from sqlalchemy import Column, Integer, table, Table

from src.database import manager


class DataORM(manager.Base):
    __abstract__ = True
    name: str = 'data'

    @classmethod
    def table(cls) -> Table: 
        return Table(cls.name, manager.Base.metadata)
    