from pydantic import BaseModel, field_validator

class MoedaCadastroSchema(BaseModel):
    """Define como uma nova moeda a ser inserida deve ser representada."""

    simbolo: str = "XYZ"
    descricao: str = "Nome da Moeda XYZ"

    @field_validator("simbolo", mode="before")
    @classmethod
    def validar_simbolo(cls, valor):
        if valor is None:
            raise ValueError("Símbolo da moeda é obrigatório.")

        valor = str(valor).strip().upper()

        if valor == "":
            raise ValueError("Símbolo da moeda é obrigatório.")

        return valor


class MoedaViewSchema(BaseModel):
    """Define como uma moeda será retornada pela API."""

    id: int
    simbolo: str
    descricao: str


class MoedaListagemSchema(BaseModel):
    """Define como uma listagem de moedas será retornada."""

    moedas: list[MoedaViewSchema]


class MoedaIdSchema(BaseModel):
    """Define como deve ser informado o ID de uma moeda."""

    id: int = 1


class MoedaDeleteSchema(BaseModel):
    """Define como será retornado o resultado da exclusão de uma moeda."""

    message: str
    simbolo: str

class MoedaSimboloSchema(BaseModel):
    simbolo: str = "USD"

def apresenta_moeda(moeda):
    """Retorna uma representação de uma moeda."""

    return {
        "id": moeda.id,
        "simbolo": moeda.simbolo,
        "descricao": moeda.descricao
    }


def apresenta_moedas(moedas):
    """Retorna uma representação da listagem de moedas."""

    result = []

    for moeda in moedas:
        result.append({
            "id": moeda.id,
            "simbolo": moeda.simbolo,
            "descricao": moeda.descricao
        })

    return {"moedas": result}