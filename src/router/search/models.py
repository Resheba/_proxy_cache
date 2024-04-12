from sqlalchemy import Column, Integer, table, Table

from src.database import manager


class DataORM(manager.Base):
    __abstract__ = True

    @staticmethod
    def table():
        data_table: Table = Table('data', manager.Base.metadata)
        return data_table
    