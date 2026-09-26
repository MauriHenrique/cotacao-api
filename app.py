from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS

from routes import (cliente_bp,moeda_bp,cotacao_bp, banco_bp)

info = Info(title="Cotação Eletrônica API",version="1.0.0")

app = OpenAPI(__name__,info=info)

CORS(app)

app.register_api(cliente_bp)
app.register_api(moeda_bp)
app.register_api(cotacao_bp)
app.register_api(banco_bp)