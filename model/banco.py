from sqlalchemy import Column, Integer, String

from model import Base


class Banco(Base):
    __tablename__ = 'banco'

    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)