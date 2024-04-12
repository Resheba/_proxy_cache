from pydantic import BaseModel


class ColumnReturn(BaseModel):
    id: int | None = None
    column_name: str
    