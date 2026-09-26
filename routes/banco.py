from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError

from model import Session
from model.banco import Banco
from model.cotacao import Cotacao

from schemas import (
    BancoCadastroSchema,
    BancoViewSchema,
    BancoBuscaSchema,
    BancoIdSchema,
    BancoEditaSchema,
    BancoDeleteSchema,
    BancosListagemSchema,
    ErrorSchema,
    apresenta_banco,
    apresenta_bancos
)

from logger import logger


banco_tag = Tag(
    name="Banco",
    description="Cadastro e consulta de bancos"
)

banco_bp = APIBlueprint(
    "banco",
    __name__,
    abp_tags=[banco_tag]
)


@banco_bp.post(
    '/cadastrar_banco',
    responses={
        "200": BancoViewSchema,
        "409": ErrorSchema,
        "400": ErrorSchema
    }
)
def add_banco(form: BancoCadastroSchema):
    """Adiciona um novo banco à base de dados."""

    banco = Banco(
        nome=form.nome
    )

    session = Session()

    try:
        session.add(banco)
        session.commit()

        logger.info(
            f"Banco '{banco.nome}' adicionado com sucesso"
        )

        return apresenta_banco(banco), 200

    except IntegrityError:
        session.rollback()

        error_msg = "Já existe um banco com este nome."

        logger.warning(error_msg)

        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível cadastrar o banco."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()


@banco_bp.get(
    '/buscar_bancos',
    responses={
        "200": BancosListagemSchema
    }
)
def get_bancos():
    """Retorna todos os bancos cadastrados."""

    logger.info("Coletando bancos")

    session = Session()

    try:
        bancos = session.query(Banco).all()

        if not bancos:
            return {"bancos": []}, 200

        logger.info(
            f"{len(bancos)} bancos encontrados"
        )

        return apresenta_bancos(bancos), 200

    finally:
        session.close()


# @banco_bp.get(
#     '/buscar_banco',
#     responses={
#         "200": BancoViewSchema,
#         "404": ErrorSchema
#     }
# )
# def get_banco(query: BancoBuscaSchema):
#     """Busca um banco pelo nome."""

#     session = Session()

#     try:
#         banco = session.query(Banco).filter(
#             Banco.nome == query.nome
#         ).first()

#         if not banco:
#             error_msg = "erro_banco."

#             logger.warning(error_msg)

#             return {"message": error_msg}, 404

#         return apresenta_banco(banco), 200

#     finally:
#         session.close()


@banco_bp.put(
    '/editar_banco',
    responses={
        "200": BancoViewSchema,
        "404": ErrorSchema,
        "409": ErrorSchema,
        "400": ErrorSchema
    }
)
def editar_banco(form: BancoEditaSchema):
    """Edita os dados de um banco."""

    session = Session()

    try:
        banco = session.query(Banco).filter(
            Banco.id == form.id
        ).first()

        if not banco:
            error_msg = "erro_banco."

            logger.warning(error_msg)

            return {"message": error_msg}, 404

        banco.nome = form.nome

        session.commit()

        logger.info(
            f"Banco #{banco.id} editado com sucesso"
        )

        return apresenta_banco(banco), 200

    except IntegrityError:
        session.rollback()

        error_msg = "Já existe um banco com este nome."

        logger.warning(error_msg)

        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível editar o banco."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()


@banco_bp.delete(
    '/deletar_banco',
    responses={
        "200": BancoDeleteSchema,
        "404": ErrorSchema,
        "409": ErrorSchema,
        "400": ErrorSchema
    }
)
def del_banco(query: BancoIdSchema):
    """Remove um banco sem cotações vinculadas.

    Retorna 409 se houver cotações vinculadas, independentemente do status.
    """

    session = Session()

    try:
        banco = session.query(Banco).filter(
            Banco.id == query.id
        ).first()

        if not banco:
            error_msg = "erro_banco."

            logger.warning(error_msg)

            return {"message": error_msg}, 404

        cotacao_vinculada = session.query(Cotacao).filter(
            Cotacao.id_banco == banco.id
        ).first()

        if cotacao_vinculada:
            error_msg = (
                "Não é possível excluir este banco porque existem "
                "cotações vinculadas."
            )
            return {"message": error_msg}, 409

        nome_banco = banco.nome

        session.delete(banco)
        session.commit()

        logger.info(
            f"Banco '{nome_banco}' removido com sucesso"
        )

        return {
            "message": "Banco removido com sucesso.",
            "nome": nome_banco
        }, 200

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível remover o banco."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()
