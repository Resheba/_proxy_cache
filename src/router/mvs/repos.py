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
        try:
            await ClientORM.drop(self.session)
            await self.session.commit()

            columns: list[str] = await ClientColumnRepository(self.session).get(only_columns=['column_name'])
            if not columns:
                await self.session.commit()
                return 'WARN: No columns found'
            
            stmt = text(f"CREATE MATERIALIZED VIEW {ClientORM.name} AS SELECT DISTINCT {', '.join(columns)} FROM data")
            await self.session.execute(stmt)
            await self.session.commit()

            # Cache reset
            try: await self.get(offset=0, limit=1) 
            except Exception: pass

            return str(stmt)
        except SQLAlchemyError as ex:
            raise BaseHTTPException(status_code=500, msg=ex._message())
        
    async def get(self, 
                  offset: int,
                  limit: int,
                  **filter_by
                  ) -> Iterable[dict]:
        try:
            stmt: Select = select(text("*")).select_from(text(ClientORM.name)).filter_by(**filter_by).offset(offset).limit(limit)
            result: Result = await self.session.execute(stmt, execution_options={'compiled_cache': None})
            data: list[Row] = result.all()
            return map(Row._asdict, data)
        except SQLAlchemyError as ex:
            raise BaseHTTPException(status_code=500, msg=ex._message())
        