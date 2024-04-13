from sqlalchemy import MetaData, Select, text, TableClause, Table, select
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement
from sqlalchemy.sql import table as table_
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql.base import PGDDLCompiler

from .utils import classproperty


class MaterializedView(DDLElement):
    name: str
    selectable: Select
    # table: TableClause = _table()

    @classproperty
    def table(cls) -> TableClause:
        t = table_(cls.name)
        t.columns._populate_separate_keys(
            col._make_proxy(t) for col in cls.selectable.selected_columns
        )
        return t
    
    @classmethod
    async def refresh(cls, session: Session) -> None:
        await session.execute(text('REFRESH MATERIALIZED VIEW %s;' % (
            cls.name
        )))

    @classmethod
    async def drop(cls, session: Session) -> None:
        await session.execute(text('DROP MATERIALIZED VIEW IF EXISTS %s;' % (
            cls.name
        )))



@compiler.compiles(MaterializedView)
def _create_m_view_compiler(element: MaterializedView, compiler: PGDDLCompiler, **kwargs) -> str:
    print(element.selectable)
    return "CREATE MATERIALIZED VIEW IF NOT EXISTS %s AS %s;" % (
        element.name,
        compiler.sql_compiler.process(element.selectable, literal_binds=True),
    )


class View(DDLElement):
    name: str
    selectable: Select
    # table: TableClause = _table()

    # @classproperty
    # def table(cls) -> TableClause:
    #     t = table_(cls.name)
    #     t.columns._populate_separate_keys(
    #         col._make_proxy(t) for col in cls.selectable.selected_columns
    #     )
    #     return t

    # @classmethod
    # def actual(cls, metadata: MetaData) -> bool:
    #     if cls.name in metadata.tables:
    #         cls.table = metadata.tables[cls.name]
    #         return True
    #     return False
    
    @classmethod
    async def drop(cls, session: Session) -> None:
        await session.execute(text('DROP VIEW IF EXISTS %s;' % (
            cls.name
        )))

    

@compiler.compiles(View)
def _create_view_compiler(element: View, compiler: PGDDLCompiler, **kwargs) -> str:
    return "CREATE OR REPLACE VIEW %s AS %s;" % (
        element.name,
        compiler.sql_compiler.process(element.selectable, literal_binds=True),
    )