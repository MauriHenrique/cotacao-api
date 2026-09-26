from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError

from model import Session
from model.cliente import Cliente
from model.cotacao import Cotacao

from schemas import (
    ClienteCadastroSchema,
    ClienteViewSchema,
    ClienteBuscaSchema,
    ClienteIdSchema,
    ClienteEditaSchema,
    ClienteDeleteSchema,
    ClientesListagemSchema,
    ErrorSchema,
    apresenta_cliente,
    apresenta_clientes
)

from logger import logger


cliente_tag = Tag(
    name="Cliente",
    description="Cadastro e consulta de clientes"
)

cliente_bp = APIBlueprint(
    "cliente",
    __name__,
    abp_tags=[cliente_tag]
)


@cliente_bp.post(
    '/cadastrar_cliente',
    responses={
        "200": ClienteViewSchema,
        "409": ErrorSchema,
        "400": ErrorSchema
    }
)
def add_cliente(form: ClienteCadastroSchema):
    """Adiciona um novo cliente à base de dados."""

    cliente = Cliente(
        nome=form.nome,
        documento=form.documento
    )

    session = Session()

    try:
        session.add(cliente)
        session.commit()

        logger.info(
            f"Cliente '{cliente.nome}' adicionado com sucesso"
        )

        return apresenta_cliente(cliente), 200

    except IntegrityError:
        session.rollback()

        error_msg = "Já existe um cliente com este documento."

        logger.warning(error_msg)

        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível cadastrar o cliente."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()


@cliente_bp.get(
    '/buscar_clientes',
    responses={
        "200": ClientesListagemSchema
    }
)
def get_clientes():
    """Retorna todos os clientes cadastrados."""

    logger.info("Coletando clientes")

    session = Session()

    try:
        clientes = session.query(Cliente).all()

        if not clientes:
            return {"clientes": []}, 200

        logger.info(
            f"{len(clientes)} clientes encontrados"
        )

        return apresenta_clientes(clientes), 200

    finally:
        session.close()


@cliente_bp.get(
    '/buscar_cliente',
    responses={
        "200": ClientesListagemSchema
    }
)
def get_cliente(query: ClienteBuscaSchema):
    """Busca clientes pelo nome."""

    session = Session()

    try:
        clientes = session.query(Cliente).filter(
            Cliente.nome.ilike(f"%{query.nome}%")
        ).all()

        return apresenta_clientes(clientes), 200

    finally:
        session.close()


@cliente_bp.put(
    '/editar_cliente',
    responses={
        "200": ClienteViewSchema,
        "404": ErrorSchema,
        "409": ErrorSchema,
        "400": ErrorSchema
    }
)
def editar_cliente(form: ClienteEditaSchema):
    """Edita os dados de um cliente."""

    session = Session()

    try:
        cliente = session.query(Cliente).filter(
            Cliente.id == form.id
        ).first()

        if not cliente:
            error_msg = "erro_cliente."

            logger.warning(error_msg)

            return {"message": error_msg}, 404

        cliente.nome = form.nome
        cliente.documento = form.documento

        session.commit()

        logger.info(
            f"Cliente #{cliente.id} editado com sucesso"
        )

        return apresenta_cliente(cliente), 200

    except IntegrityError:
        session.rollback()

        error_msg = "Já existe um cliente com este documento."

        logger.warning(error_msg)

        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível editar o cliente."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()


@cliente_bp.delete(
    '/deletar_cliente',
    responses={
        "200": ClienteDeleteSchema,
        "404": ErrorSchema,
        "409": ErrorSchema,
        "400": ErrorSchema
    }
)
def del_cliente(query: ClienteIdSchema):
    """Remove um cliente sem cotações vinculadas.

    Retorna 409 se houver cotações vinculadas, independentemente do status.
    """

    session = Session()

    try:
        cliente = session.query(Cliente).filter(
            Cliente.id == query.id
        ).first()

        if not cliente:
            error_msg = "erro_cliente."

            logger.warning(error_msg)

            return {"message": error_msg}, 404

        cotacao_vinculada = session.query(Cotacao).filter(
            Cotacao.id_cliente == cliente.id
        ).first()

        if cotacao_vinculada:
            error_msg = (
                "Não é possível excluir este cliente porque existem "
                "cotações vinculadas."
            )
            return {"message": error_msg}, 409

        nome_cliente = cliente.nome

        session.delete(cliente)
        session.commit()

        logger.info(
            f"Cliente '{nome_cliente}' removido com sucesso"
        )

        return {
            "message": "Cliente removido com sucesso.",
            "nome": nome_cliente
        }, 200

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível remover o cliente."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()
