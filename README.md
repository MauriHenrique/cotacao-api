
## API - Cotação Eletrônica

API desenvolvida em Python para gerenciar cotações de operações de câmbio.


Este projeto foi desenvolvido como parte de um trabalho da pós-graduação.

### Tecnologias

- Python
- Flask
- Flask-OpenAPI3
- Flask-SQLAlchemy / SQLAlchemy
- Flask-CORS
- Pydantic
- SQLite
- Requests



#### Clientes

- Cadastrar clientes
- Listar clientes
- Pesquisar clientes pelo nome
- Editar clientes
- Excluir clientes

#### Bancos

- Cadastrar bancos
- Listar bancos
- Editar bancos
- Excluir bancos

#### Moedas

- Cadastrar moedas
- Listar moedas
- Excluir moedas

#### Cotações

- Cadastrar cotações
- Listar cotações
- Consultar a taxa de câmbio
- Aceitar cotações
- Cancelar cotações
- Excluir cotações
- Controlar a validade das cotações

As cotações podem apresentar os seguintes status:

- ATIVA
- ACEITA
- CANCELADA
- EXPIRADA (baseada no tempo, validade de 10min)

### Estrutura do projeto

```text
api/
├── database/
├── log/
├── model/
├── routes/
├── schemas/
├── app.py
├── logger.py
├── requirements.txt
└── README.md
```

### Requisitos

- Python 3.14
- pip

### Instalação

#### 1. Baixar o projeto

Clone o repositório ou baixe os arquivos para o computador do githud.

#### 2. Criar o ambiente virtual

Abra o terminal na pasta do projeto e execute:

```powershell
python -m venv mvp
```

#### 3. Ativa o ambiente virtual

No Windows:

```powershell
.\mvp\Scripts\Activate.ps1
ou 
deactivate  (para desativar)
```

#### 4. Instalar as dependências

Entre na pasta da API:

```powershell
cd api
ou a pasta da API
```

Instale as bibliotecas:

```powershell
pip install -r requirements.txt
```

Recria o banco quando apagado (para testes):

```powershell
python -c "import model"
```

#### Executar a API

Com o ambiente virtual ativado e o terminal na pasta `api`, execute:

```powershell
flask run --host 127.0.0.1 --port 5000
```

A API está disponível em:

http://127.0.0.1:5000

####  Swagger

A documentação interativa da API pode ser acessada em:

http://127.0.0.1:5000/openapi/swagger

O Swagger permite consultar as rotas, visualizar os parâmetros e testar as requisições.

#### Banco de dados

O projeto utiliza SQLite.

O banco de dados fica na pasta:

```text
database/db.sqlite3
```

As tabelas são criadas automaticamente pelo SQLAlchemy quando o projeto é inicializado, caso ainda não existam.

### Rotas

#### Clientes

| Método | Rota |
|---     |---|
| POST   | /cadastrar_cliente |
| GET    | /buscar_clientes |
| GET    | /buscar_cliente |
| PUT    | /editar_cliente |
| DELETE | /deletar_cliente |

#### Bancos

| Método | Rota |
|---     |---|
| POST   | /cadastrar_banco |
| GET    | /buscar_bancos |
| PUT    | /editar_banco |
| DELETE | /deletar_banco |

#### Moedas

| Método | Rota |
|---     |---|
| POST   | /cadastrar_moeda |
| GET    | /buscar_moedas |
| DELETE | /deletar_moeda |

#### Cotações

| Método | Rota |
|---     |---|
| POST   | /cadastrar_cotacao |
| GET    | /buscar_cotacoes |
| GET    | /buscar_taxa |
| PUT    |  /aceitar_cotacao |
| PUT    | /cancelar_cotacao |
| DELETE | /deletar_cotacao |

Os parâmetros e os formatos das requisições estão documentados no Swagger.

### ** ATENÇÃO **

#### Consulta de taxas externa

A consulta da taxa de referencia utiliza uma API pública externa (Frankfurter) para obter a cotação de uma moeda em relação ao real (R$).

Ela é feira por uma conexão HTTPS, o parâmetro verify=False desativa a validação do certificado SSL, caja aja problama na conexão.

***routes\cotacao.py***

    #response = requests.get(url, timeout=10)
    response = requests.get(url, timeout=10, verify=False)

Obs.: essa consulta é opcional, podendo ser inserida manualmente.

