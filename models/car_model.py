from reusable.index import Base, Utility
from sqlalchemy import Column, Integer, String


class CarModel(Base, Utility):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    colour = Column(String(100), default='black')
    model = Column(String(100), nullable=False)
    name = Column(String(120), nullable=False, unique=True)
    year = Column(Integer, nullable=False)
