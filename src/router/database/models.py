from sqlalchemy import Select, select, Column, Integer, String

from src.database._view import MaterializedView
from src.database import manager


class ClientColumnORM(manager.Base):
    __tablename__ = 'client_column'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    column_name = Column(String, nullable=False, unique=True)


class WorkPlaceColumnORM(manager.Base):
    __tablename__ = 'workplace_column'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    column_name = Column(String, nullable=False, unique=True)


class ProfessionColumnORM(manager.Base):
    __tablename__ = 'profession_column'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    column_name = Column(String, nullable=False, unique=True)


# class ClientsORM(MaterializedView):
#     name = 'client'
#     selectable = select([MaterializedView.table.columns.client_id])