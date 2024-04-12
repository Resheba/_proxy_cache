from pydantic import BaseModel
from typing import Any, Sequence, Type
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Delete, Result, Select, delete, select, inspect, text
from sqlalchemy.ext.asyncio import AsyncSession


class Repository:
    orm_model: Type[DeclarativeBase]
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def create(self, 
                     data: Type[BaseModel]
                     ) -> Any:
        obj = self.orm_model(**data.model_dump(exclude_unset=True))
        self.session.add(obj)
        await self.session.commit()
        return obj
    
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
                     pk_list: Sequence[Any]
                     ) -> None:
        stmt: Delete = delete(self.orm_model).where(inspect(self.orm_model).primary_key[0].in_(pk_list))
        await self.session.execute(stmt)
        await self.session.commit()    
