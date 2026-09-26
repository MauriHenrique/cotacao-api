from sqlalchemy import Column, String, Integer

from  model import Base


class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True)
    nome = Column(String(500))
    documento = Column(String(20), nullable=False, unique=True)

    def __init__(self, nome:str, documento:str):
        """
        Cria um Cliente

        Arguments:
            nome: o nome do cliente.
            documento: CPF ou CNPJ do cliente.
        """
        self.nome = nome
        self.documento = documento
