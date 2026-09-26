from typing import List
from pydantic import BaseModel, field_validator


class ClienteCadastroSchema(BaseModel):
    """Define como um novo cliente a ser inserido deve ser representado."""

    nome: str = "Empresa Exemplo Ltda"
    documento: str = "12345678000199"

    @field_validator("documento", mode="before")
    @classmethod
    def validar_documento(cls, valor):
        if valor is None:
            raise ValueError("Documento é obrigatório.")

        valor = str(valor).strip()

        if valor == "":
            raise ValueError("Documento é obrigatório.")

        return valor



class ClienteViewSchema(BaseModel):
    id: int 
    nome: str
    documento: str

class ClienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do cliente.
    """
    nome: str = "Empresa Exemplo Ltda"

class ClienteIdSchema(BaseModel):
    """Define como deve ser informado o ID de um cliente."""

    id: int = 1

class ClientesListagemSchema(BaseModel):
    clientes: List[ClienteViewSchema]


class ClienteDeleteSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção. """
    
    message: str
    nome: str

class ClienteEditaSchema(BaseModel):
    """Define como deve ser representada a edição de um cliente."""

    id: int = 1
    nome: str = "Empresa Exemplo Ltda"
    documento: str = "12345678000199"

    @field_validator("documento", mode="before")
    @classmethod
    def validar_documento(cls, valor):
        if valor is None:
            raise ValueError("Documento é obrigatório.")

        valor = str(valor).strip()

        if valor == "":
            raise ValueError("Documento é obrigatório.")

        return valor

def apresenta_clientes(clientes: List):
    result = []

    for cliente in clientes:
        result.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "documento": cliente.documento
        })

    return {"clientes": result}

def apresenta_cliente(cliente):
    """Retorna uma representação de um cliente."""

    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "documento": cliente.documento
    }
