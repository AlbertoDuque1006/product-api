# Product API

Repositorio PÚBLICO de portafolio: https://github.com/AlbertoDuque1006/product-api (rama `main`, licencia MIT). Es una API REST serverless de aprendizaje: `GET /products/{id}` con API Gateway y Lambda (Python 3.12), definida con AWS CDK. Los productos viven en memoria (`lambda_code/productos.py`). Responde siempre en español; el README está en inglés y así se queda.

- `lambda_code/`: el handler (`get_product.py`), los datos y `responses.py` (JSON + CORS).
- `product_api/product_api_stack.py`: la infraestructura (CDK).
- `tests/unit/`: prueba del stack (`pytest`).
- Comandos: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt`, `pytest`, `cdk synth`, `cdk diff`, `cdk deploy`.
- Mejoras posibles (están en el README): CRUD completo, DynamoDB, validación, autenticación, CI con GitHub Actions y varios ambientes.

Reglas: nunca subir credenciales de AWS, el ID de la cuenta ni `.env`. Commits solo con la cuenta AlbertoDuque1006 (config local del repo).
