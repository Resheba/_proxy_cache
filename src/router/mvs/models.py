from sqlalchemy import text

from src.database._view import MaterializedView, View


class ClientORM(MaterializedView):
    name = 'client'
    # selectable = text('SELECT DISTINCT clientid, clientname FROM data')
    