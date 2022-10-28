from domain.db import DBSession
from domain.db import Base


class DBInterface:
    def __init__(self, db_class: type[Base]):
        self.db_class = db_class

    def read_all(self):
        session = DBSession()
        user: Base = session.query(self.db_class).all()
        session.close()
        return user
