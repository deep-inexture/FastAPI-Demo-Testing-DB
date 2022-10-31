from domain.db import Base
from sqlalchemy import String, Integer, Column, Boolean

"""
This files stores schemas of tables like tableName, tableColumn, and its Datatype.
Main file sees into this file first for each non created table to be generated or not.
"""


class User(Base):
    """This Table has user details for authentication and access purpose."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
