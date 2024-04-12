from sqlalchemy import Column, Integer, table, Table

from src.database import manager


class DataORM(manager.Base):
    __abstract__ = True
    # __tablename__ = "data"
    # __table__ = manager.Base.metadata.tables["data"]
    # __table_args__ = {"autoload_with": manager.engine}

    # id = Column(Integer, primary_key=True)
    @staticmethod
    def table():
        data_table: Table = Table('data', manager.Base.metadata)
        return data_table
    