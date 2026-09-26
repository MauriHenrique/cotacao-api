import requests

from datetime import datetime, timedelta

from flask_openapi3 import APIBlueprint, Tag

from model import Session
from model.cliente import Cliente
from model.banco import Banco
from model.moeda import Moeda
from model.cotacao import Cotacao

from schemas import (
    CotacaoCadastroSchema,
    CotacaoViewSchema,
    CotacaoListagemSchema,
    CotacaoIdSchema,
    CotacaoExternaSchema,
    MoedaSimboloSchema,
    ErrorSchema,
    apresenta_cotacao,
    apresenta_cotacoes
)

from logger import logger


cotacao_tag = Tag(
    name="Cotação",
    description="Cadastro e gerenciamento de cotações"
)

cotacao_bp = APIBlueprint(
    "cotacao",
    __name__,
    abp_tags=[cotacao_tag]
)


@cotacao_bp.post(
    '/cadastrar_cotacao',
    responses={
        "200": CotacaoViewSchema,
        "404": ErrorSchema,
        "400": ErrorSchema
    }
)
def add_cotacao(form: CotacaoCadastroSchema):
    """Adiciona uma nova cotação à base de dados."""

    session = Session()

    try:
        cliente = session.query(Cliente).filter(
            Cliente.id == form.id_cliente
        ).first()

        if not cliente:
            error_msg = "erro_cliente."

            logger.warning(error_msg)

            return {"message": error_msg}, 404

        banco = session.query(Banco).filter(
            Banco.id == form.id_banco
        ).first()

        if not banco:
            error_msg = "erro_banco."

            logger.warning(error_msg)

            return {"message": error_msg}, 404

        moeda = session.query(Moeda).filter(
            Moeda.id == form.id_moeda
        ).first()

        if not moeda:
            error_msg = "erro_moeda"

            logger.warning(error_msg)

            return {"message": error_msg}, 404

        data_criacao = datetime.now()

        data_expiracao = (
            data_criacao +
            timedelta(minutes=form.validade)
        )

        valor_mn = (
            form.valor_me *
            form.taxa_oferecida
        )

        spread = (
            (
                form.taxa_oferecida -
                form.taxa_referencia
            )
            /
            form.taxa_referencia
        ) * 100

        codigo = data_criacao.strftime(
            "RL-%Y%m%d-%H%M%S"
        )

        cotacao = Cotacao(
            codigo=codigo,
            id_cliente=form.id_cliente,
            id_banco=form.id_banco,
            id_moeda=form.id_moeda,
            tipo_operacao=form.tipo_operacao,
            valor_me=form.valor_me,
            taxa_referencia=form.taxa_referencia,
            taxa_oferecida=form.taxa_oferecida,
            spread=spread,
            valor_mn=valor_mn,
            data_expiracao=data_expiracao
        )

        session.add(cotacao)
        session.commit()

        logger.info(
            f"Cotação '{cotacao.codigo}' cadastrada com sucesso"
        )

        return apresenta_cotacao(cotacao), 200

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível cadastrar a cotação."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()


@cotacao_bp.get(
    '/buscar_cotacoes',
    responses={
        "200": CotacaoListagemSchema,
        "400": ErrorSchema
    }
)
def get_cotacoes():
    """Retorna todas as cotações cadastradas."""

    logger.info("Coletando cotações")

    session = Session()

    try:
        agora = datetime.now()

        cotacoes_expiradas = session.query(Cotacao).filter(
            Cotacao.status == "ATIVA",
            Cotacao.data_expiracao <= agora
        ).all()

        for cotacao in cotacoes_expiradas:
            cotacao.status = "EXPIRADA"
            cotacao.data_status = cotacao.data_expiracao

        if cotacoes_expiradas:
            session.commit()

            logger.info(
                f"{len(cotacoes_expiradas)} cotações "
                "marcadas como expiradas"
            )

        cotacoes = session.query(Cotacao).order_by(
            Cotacao.data_criacao.desc()
        ).all()

        if not cotacoes:
            return {"cotacoes": []}, 200

        logger.info(
            f"{len(cotacoes)} cotações encontradas"
        )

        return apresenta_cotacoes(cotacoes), 200

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível buscar as cotações."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()


@cotacao_bp.put(
    '/aceitar_cotacao',
    responses={
        "200": CotacaoViewSchema,
        "404": ErrorSchema,
        "400": ErrorSchema
    }
)
def aceitar_cotacao(query: CotacaoIdSchema):
    """Aceita uma cotação ativa."""

    session = Session()

    try:
        cotacao = session.query(Cotacao).filter(
            Cotacao.id == query.id
        ).first()

        if not cotacao:
            error_msg = "erro_cotacao"

            logger.warning(error_msg)

            return {"message": error_msg}, 404

        if cotacao.status != "ATIVA":
            error_msg = (
                "Somente cotações ativas podem ser aceitas."
            )

            logger.warning(error_msg)

            return {"message": error_msg}, 400

        if cotacao.data_expiracao <= datetime.now():
            cotacao.status = "EXPIRADA"
            cotacao.data_status = cotacao.data_expiracao

            session.commit()

            error_msg = "A cotação já está expirada."

            logger.warning(error_msg)

            return {"message": error_msg}, 400

        cotacao.status = "ACEITA"
        cotacao.data_status = datetime.now()

        session.commit()

        logger.info(
            f"Cotação '{cotacao.codigo}' aceita com sucesso"
        )

        return apresenta_cotacao(cotacao), 200

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível aceitar a cotação."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()


@cotacao_bp.put(
    '/cancelar_cotacao',
    responses={
        "200": CotacaoViewSchema,
        "404": ErrorSchema,
        "400": ErrorSchema
    }
)
def cancelar_cotacao(query: CotacaoIdSchema):
    """Cancela uma cotação ativa."""

    session = Session()

    try:
        cotacao = session.query(Cotacao).filter(
            Cotacao.id == query.id
        ).first()

        if not cotacao:
            error_msg = "erro_cotacao"

            logger.warning(error_msg)

            return {"message": error_msg}, 404

        if cotacao.status != "ATIVA":
            error_msg = (
                "Somente cotações ativas podem ser canceladas."
            )

            logger.warning(error_msg)

            return {"message": error_msg}, 400

        if cotacao.data_expiracao <= datetime.now():
            cotacao.status = "EXPIRADA"
            cotacao.data_status = cotacao.data_expiracao

            session.commit()

            error_msg = "A cotação já está expirada."

            logger.warning(error_msg)

            return {"message": error_msg}, 400

        cotacao.status = "CANCELADA"
        cotacao.data_status = datetime.now()

        session.commit()

        logger.info(
            f"Cotação '{cotacao.codigo}' cancelada com sucesso"
        )

        return apresenta_cotacao(cotacao), 200

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível cancelar a cotação."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()


@cotacao_bp.delete(
    '/deletar_cotacao',
    responses={
        "200": ErrorSchema,
        "404": ErrorSchema,
        "400": ErrorSchema
    }
)
def deletar_cotacao(query: CotacaoIdSchema):
    """Exclui uma cotação da base de dados."""

    session = Session()

    try:
        cotacao = session.query(Cotacao).filter(
            Cotacao.id == query.id
        ).first()

        if not cotacao:
            error_msg = "erro_cotacao"

            logger.warning(error_msg)

            return {"message": error_msg}, 404

        codigo = cotacao.codigo

        session.delete(cotacao)
        session.commit()

        logger.info(
            f"Cotação '{codigo}' excluída com sucesso"
        )

        return {
            "message": "Cotação excluída com sucesso."
        }, 200

    except Exception as e:
        session.rollback()

        error_msg = "Não foi possível excluir a cotação."

        logger.error(
            f"{error_msg} Erro: {str(e)}"
        )

        return {"message": error_msg}, 400

    finally:
        session.close()

@cotacao_bp.get(
    '/buscar_taxa',
    responses={
        "200": CotacaoExternaSchema,
        "400": ErrorSchema
    }
)
def buscar_taxa(query: MoedaSimboloSchema):
    """Consulta a taxa atual da moeda em relação ao Real."""

    try:
        simbolo = query.simbolo.strip().upper()

        url = (
            f"https://api.frankfurter.dev/v2/rates"
            f"?base={simbolo}&quotes=BRL"
        )

        #response = requests.get(url, timeout=10)
        response = requests.get(url, timeout=10, verify=False)
        
        response.raise_for_status()

        dados = response.json()

        if not dados:
            return {
                "message": "erro_cotacao"
            }, 400

        taxa = dados[0]["rate"]

        logger.info(
            f"Cotação externa {simbolo}/BRL: {taxa}"
        )

        return {
            "simbolo": simbolo,
            "taxa": taxa
        }, 200

    except Exception as e:
        logger.error(
            f"Erro ao consultar cotação externa: {str(e)}"
        )

        return {
            "message": "Não foi possível consultar a cotação externa."
        }, 400