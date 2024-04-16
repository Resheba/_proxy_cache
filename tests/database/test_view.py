import pytest
from sqlalchemy import select, text

from src.database._view import MaterializedView


def test_view():
    MaterializedView.selectable = select(text('*')).select_from(text('test'))
    MaterializedView.name = 'test'

    assert MaterializedView().compile().__str__() == 'CREATE MATERIALIZED VIEW IF NOT EXISTS test AS SELECT * \nFROM test;'


@pytest.mark.asyncio
async def test_view_refresh():
    with pytest.raises(TypeError):
        await MaterializedView().refresh()

    
@pytest.mark.asyncio
async def test_view_drop():
    with pytest.raises(TypeError):
        await MaterializedView().drop()
        