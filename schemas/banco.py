from pydantic import BaseModel
from typing import List


class BancoCadastroSchema(BaseModel):
    """Define como um novo banco deve ser cadastrado."""
    nome: str


class BancoViewSchema(BaseModel):
    """Define como um banco será retornado."""
    id: int
    nome: str


class BancoBuscaSchema(BaseModel):
    """Define a busca de um banco pelo nome."""
    nome: str


class BancoIdSchema(BaseModel):
    """Define a busca de um banco pelo ID."""
    id: int


class BancoEditaSchema(BaseModel):
    """Define os dados para edição de um banco."""
    id: int
    nome: str


class BancoDeleteSchema(BaseModel):
    """Define o retorno após a exclusão de um banco."""
    message: str
    nome: str


class BancosListagemSchema(BaseModel):
    """Define a listagem de bancos."""
    bancos: List[BancoViewSchema]


def apresenta_banco(banco):
    """Retorna a representação de um banco."""

    return {
        "id": banco.id,
        "nome": banco.nome
    }


def apresenta_bancos(bancos):
    """Retorna a representação de uma lista de bancos."""

    return {
        "bancos": [
            apresenta_banco(banco)
            for banco in bancos
        ]
    }