from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.cliente import Cliente
from model.cotacao import Cotacao
from model.moeda import Moeda
from model.banco import Banco

db_path = "database/"

# Verifica se o diretorio não existe
if not os.path.exists(db_path):
    # então cria o diretorio
    os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de sessão com o banco
Session = sessionmaker(bind=engine)

# cria o banco e as tabelas, caso não existam
Base.metadata.create_all(engine)