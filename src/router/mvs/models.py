from sqlalchemy import text

from src.database._view import MaterializedView


class ClientORM(MaterializedView):
    name = 'client'
    

class WorkPlaceORM(MaterializedView):
    name = 'workplace'


class ProfessionORM(MaterializedView):
    name = 'profession'
    