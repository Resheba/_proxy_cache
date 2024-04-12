from typing import Iterable
from sqlalchemy import Result, select, Select, Text, Row, Table, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import BaseHTTPException

from .models import DataORM


class DataRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get(self,
                  *, 
                  query: str | None = None,
                  offset: int,
                  limit: int,
                  **filter_by
                  ) -> Iterable[DataORM]:
        try:
            table: Table = DataORM.table()
            stmt: Select = select(table).filter_by(**filter_by).offset(offset).limit(limit)
            if query:
                stmt = (stmt.where(
                    func.to_tsvector('russian', table.table_valued().cast(Text))
                    .op('@@')
                    (func.plainto_tsquery('russian', query))
                    )
                )
            result: Result = await self.session.execute(stmt)
            data: list[Row] = result.all()
            return map(Row._asdict, data)
        except SQLAlchemyError as ex:
            raise BaseHTTPException(status_code=500, msg=ex._message())
        