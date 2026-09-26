# from model import cliente
from pydantic import BaseModel, field_validator
from datetime import datetime


class CotacaoCadastroSchema(BaseModel):
    """Define como uma nova cotação a ser inserida deve ser representada."""

    id_cliente: int = 1
    id_moeda: int = 1
    tipo_operacao: str = "COMPRA"
    valor_me: float = 10000.00
    taxa_referencia: float = 5.4231
    taxa_oferecida: float = 5.4500
    validade: int = 10
    id_banco: int = 1

    @field_validator("tipo_operacao", mode="before")
    @classmethod
    def validar_tipo_operacao(cls, valor):
        if valor is None:
            raise ValueError("Tipo de operação é obrigatório.")

        valor = str(valor).strip().upper()

        if valor not in ["COMPRA", "VENDA"]:
            raise ValueError("Tipo de operação deve ser COMPRA ou VENDA.")

        return valor


class CotacaoViewSchema(BaseModel):
    """Define como uma cotação será retornada pela API."""

    id: int
    codigo: str

    id_cliente: int
    cliente: str

    id_banco: int
    banco: str

    id_moeda: int
    moeda: str

    tipo_operacao: str
    valor_me: float

    taxa_referencia: float
    taxa_oferecida: float
    spread: float
    valor_mn: float

    data_criacao: datetime
    data_expiracao: datetime

    status: str
    data_status: datetime




class CotacaoListagemSchema(BaseModel):
    """Define como uma listagem de cotações será retornada."""

    cotacoes: list[CotacaoViewSchema]


class CotacaoIdSchema(BaseModel):
    """Define como deve ser informado o ID de uma cotação."""

    id: int = 1

class CotacaoExternaSchema(BaseModel):
    simbolo: str
    taxa: float

def apresenta_cotacao(cotacao):
    """Retorna JSON representando uma cotação."""

    return {
        "id": cotacao.id,
        "codigo": cotacao.codigo,
        "id_cliente": cotacao.id_cliente,
        "cliente": cotacao.cliente.nome if cotacao.cliente is not None else "erro_cliente",
        "id_banco": cotacao.id_banco,
        "banco": cotacao.banco.nome if cotacao.banco is not None else "erro_banco",
        "id_moeda": cotacao.id_moeda,
        "moeda": cotacao.moeda.simbolo if cotacao.moeda is not None else "Moeda não encontrada",
        "tipo_operacao": cotacao.tipo_operacao,
        "valor_me": float(cotacao.valor_me),
        "taxa_referencia": float(cotacao.taxa_referencia),
        "taxa_oferecida": float(cotacao.taxa_oferecida),
        "spread": float(cotacao.spread),
        "valor_mn": float(cotacao.valor_mn),
        "data_criacao": cotacao.data_criacao,
        "data_expiracao": cotacao.data_expiracao,
        "status": cotacao.status,
        "data_status": cotacao.data_status
    }


def apresenta_cotacoes(cotacoes):
    """Retorna uma representação da listagem de cotações."""

    result = []

    for cotacao in cotacoes:
        result.append(apresenta_cotacao(cotacao))

    return {"cotacoes": result}
