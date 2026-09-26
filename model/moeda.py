from sqlalchemy import Column, String, Integer

from  model import Base


class Moeda(Base):
    __tablename__ = 'moeda'

    id = Column(Integer, primary_key=True)
    simbolo = Column(String(3), nullable=False, unique=True)
    descricao = Column(String(100), nullable=False, unique=True)

    def __init__(self, simbolo:str, descricao:str):
        """
        Cria uma Moeda

        Arguments:
            simbolo: o símbolo da moeda.
            descricao: a descrição da moeda.
        """
        self.simbolo = simbolo
        self.descricao = descricao
