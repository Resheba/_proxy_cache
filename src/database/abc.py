from pydantic import BaseModel
from typing import Any, Sequence, Type, Iterable
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import DDLElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Delete, Result, Select, delete, select, inspect, text, Row

from src.core import BaseHTTPException


class Repository:
    orm_model: Type[DeclarativeBase]
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def create(self, 
                     data: BaseModel | Sequence[BaseModel]
                     ) -> Any:
        try:
            if issubclass(type(data), Sequence):
                obj = [self.orm_model(**dto.model_dump(exclude_unset=True)) for dto in data]
                self.session.add_all(obj)
            else:
                obj = self.orm_model(**data.model_dump(exclude_unset=True))
                self.session.add(obj)
            await self.session.commit()
            return obj
        except SQLAlchemyError as ex:
            raise BaseHTTPException(status_code=409, msg=ex._message())
    
    async def get(self,
                  many: bool = True,
                  only_columns: list[str] | None = None,
                  **filter_by
                  ) -> Any:
        if only_columns:
            stmt: Select = select(*[text(c) for c in only_columns]).select_from(self.orm_model).filter_by(**filter_by)
        else:
            stmt: Select = select(self.orm_model).filter_by(**filter_by)
        if many:
            result: Result = await self.session.execute(stmt)
            return result.scalars().all()
        result: Result = await self.session.execute(stmt.limit(1))
        return result.scalar_one_or_none()
    
    async def delete(self,
                     pk_list: Sequence[Any] | None = None
                     ) -> None:
        if pk_list:
            stmt: Delete = delete(self.orm_model).where(inspect(self.orm_model).primary_key[0].in_(pk_list))
        else:
            stmt: Delete = delete(self.orm_model)
        await self.session.execute(stmt)
        await self.session.commit()    


class ViewRepository:
    orm_model: Type[DDLElement]
    columns_repository: type[Repository]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def replace(self) -> str:
        try:
            await self.orm_model.drop(self.session)
            await self.session.commit()

            columns: list[str] = await self.columns_repository(self.session).get(only_columns=['column_name'])
            if not columns:
                await self.session.commit()
                return 'WARN: No columns found'
            
            stmt = text(f"CREATE MATERIALIZED VIEW {self.orm_model.name} AS SELECT DISTINCT {', '.join(columns)} FROM data")
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
            stmt: Select = select(text("*")).select_from(text(self.orm_model.name)).filter_by(**filter_by).offset(offset).limit(limit)
            result: Result = await self.session.execute(stmt, execution_options={'compiled_cache': None})
            data: list[Row] = result.all()
            return map(Row._asdict, data)
        except SQLAlchemyError as ex:
            raise BaseHTTPException(status_code=500, msg=ex._message())
        