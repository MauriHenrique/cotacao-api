from flask_openapi3 import APIBlueprint, Tag
# from pydantic.v1 import BaseModel
from sqlalchemy.exc import IntegrityError

from model import Session
from model.moeda import Moeda
from model.cotacao import Cotacao

from schemas import (
    MoedaCadastroSchema,
    MoedaViewSchema,
    MoedaListagemSchema,
    MoedaIdSchema,
    MoedaDeleteSchema,
    ErrorSchema,
    apresenta_moeda,
    apresenta_moedas
)

from logger import logger


moeda_tag = Tag(
    name="Moeda",
    description="Cadastro e consulta de moedas"
)

moeda_bp = APIBlueprint(
    "moeda",
    __name__,
    abp_tags=[moeda_tag]
)


@moeda_bp.post(
    '/cadastrar_moeda',
    responses={
        "200": MoedaViewSchema,
        "409": ErrorSchema,
        "400": ErrorSchema
    }
)
def add_moeda(form: MoedaCadastroSchema):
    """Adiciona uma nova moeda à base de dados."""

    moeda = Moeda(
        simbolo=form.simbolo,
        descricao=form.descricao
    )

    session = Session()

    try:
        session.add(moeda)
        session.commit()

        logger.info(
            f"Moeda '{moeda.simbolo}' cadastrada com sucesso"
        )

        return apresenta_moeda(moeda), 200

    except IntegrityError:
        session.rollback()

        error_msg = "Já existe uma moeda com este símbolo ou descrição."

        logger.warning(error_msg)

        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível cadastrar a moeda."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()


@moeda_bp.get(
    '/buscar_moedas',
    responses={
        "200": MoedaListagemSchema
    }
)
def get_moedas():
    """Retorna todas as moedas cadastradas."""

    logger.info("Coletando moedas")

    session = Session()

    try:
        moedas = session.query(Moeda).all()

        if not moedas:
            return {"moedas": []}, 200

        logger.info(
            f"{len(moedas)} moedas encontradas"
        )

        return apresenta_moedas(moedas), 200

    finally:
        session.close()


@moeda_bp.delete(
    '/deletar_moeda',
    responses={
        "200": MoedaDeleteSchema,
        "404": ErrorSchema,
        "409": ErrorSchema,
        "400": ErrorSchema
    }
)
def del_moeda(query: MoedaIdSchema):
    """Remove uma moeda sem cotações vinculadas.

    Retorna 409 se houver cotações vinculadas, independentemente do status.
    """

    session = Session()

    try:
        moeda = session.query(Moeda).filter(
            Moeda.id == query.id
        ).first()

        if not moeda:
            error_msg = "erro_moeda"

            logger.warning(error_msg)

            return {"message": error_msg}, 404

        cotacao_vinculada = session.query(Cotacao).filter(
            Cotacao.id_moeda == moeda.id
        ).first()

        if cotacao_vinculada:
            error_msg = (
                "Não é possível excluir esta moeda porque existem "
                "cotações vinculadas."
            )
            return {"message": error_msg}, 409

        simbolo_moeda = moeda.simbolo

        session.delete(moeda)
        session.commit()

        logger.info(
            f"Moeda '{simbolo_moeda}' removida com sucesso"
        )

        return {
            "message": "Moeda removida com sucesso.",
            "simbolo": simbolo_moeda
        }, 200

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível remover a moeda."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()
