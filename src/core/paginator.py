from typing import Annotated, Any
from fastapi import Query


class PaginatorPage:
    def __init__(
            self,
            page_size: Annotated[int, Query(ge=1)] = 10,
            page_num: Annotated[int, Query(ge=1)] = 1
            ) -> None:
        self.page_size = page_size; self.page_num = page_num    
