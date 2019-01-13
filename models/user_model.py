from reusable.index import Base, Utility
from sqlalchemy import Column, Integer, String


class UserModel(Base, Utility):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    name = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
