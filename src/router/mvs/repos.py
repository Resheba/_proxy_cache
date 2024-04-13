from typing import Iterable
from sqlalchemy import Result, Row, Select, TextClause, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import BaseHTTPException

from .models import ClientORM
from ..database.repos import ClientColumnRepository


class ClientsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def replace(self) -> str:
        await ClientORM.drop(self.session)

        columns: list[str] = await ClientColumnRepository(self.session).get(only_columns=['column_name'])
        if not columns:
            await self.session.commit()
            return 'WARN: No columns found'
        
        stmt = text(f"CREATE MATERIALIZED VIEW {ClientORM.name} AS SELECT DISTINCT {', '.join(columns)} FROM data")

        await self.session.execute(stmt)
        await self.session.commit()
        return str(stmt)
    
    async def get(self, 
                  offset: int,
                  limit: int,
                  **filter_by
                  ) -> Iterable[dict]:
        try:
            stmt: Select = select(text("*")).select_from(text(ClientORM.name)).filter_by(**filter_by).offset(offset).limit(limit)
            result: Result = await self.session.execute(stmt)
            data: list[Row] = result.all()
            return map(Row._asdict, data)
        except SQLAlchemyError as ex:
            raise BaseHTTPException(status_code=500, msg=ex._message())
        