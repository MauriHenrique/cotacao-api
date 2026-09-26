from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from model import Base


class Cotacao(Base):
    __tablename__ = 'cotacao'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(30), nullable=False, unique=True)

    id_cliente = Column(
        Integer,
        ForeignKey("cliente.id"),
        nullable=False
    )

    id_banco = Column(
        Integer,
        ForeignKey("banco.id"),
        nullable=False
    )

    id_moeda = Column(
        Integer,
        ForeignKey("moeda.id"),
        nullable=False
    )

    cliente = relationship("Cliente")
    banco = relationship("Banco")
    moeda = relationship("Moeda")

    tipo_operacao = Column(String(10), nullable=False)

    valor_me = Column(Numeric(18, 2), nullable=False)

    taxa_referencia = Column(Numeric(18, 4), nullable=False)
    taxa_oferecida = Column(Numeric(18, 4), nullable=False)
    spread = Column(Numeric(10, 4), nullable=False)
    valor_mn = Column(Numeric(18, 2), nullable=False)
    data_criacao = Column(DateTime,nullable=False,default=datetime.now)
    data_expiracao = Column(DateTime,nullable=False)
    status = Column(String(15),nullable=False,default="ATIVA")
    data_status = Column(DateTime,nullable=False,default=datetime.now)

    def __init__(
        self,
        codigo: str,
        id_cliente: int,
        id_banco: int,
        id_moeda: int,
        tipo_operacao: str,
        valor_me,
        taxa_referencia,
        taxa_oferecida,
        spread,
        valor_mn,
        data_expiracao
    ):
        """
        Cria uma Cotação.

        Arguments:
            codigo: código identificador da cotação.
            id_cliente: identificador do cliente.
            id_banco: identificador do banco.
            id_moeda: identificador da moeda.
            tipo_operacao: tipo da operação, COMPRA ou VENDA.
            valor_me: valor em moeda estrangeira.
            taxa_referencia: taxa obtida da fonte externa.
            taxa_oferecida: taxa oferecida ao cliente.
            spread: percentual de spread aplicado.
            valor_mn: valor total em moeda nacional.
            data_expiracao: data e hora de expiração da cotação.
        """

        self.codigo = codigo
        self.id_banco = id_banco
        self.id_cliente = id_cliente
        self.id_moeda = id_moeda
        self.tipo_operacao = tipo_operacao
        self.valor_me = valor_me
        self.taxa_referencia = taxa_referencia
        self.taxa_oferecida = taxa_oferecida
        self.spread = spread
        self.valor_mn = valor_mn

        self.data_criacao = datetime.now()
        self.data_expiracao = data_expiracao

        self.status = "ATIVA"
        self.data_status = datetime.now()