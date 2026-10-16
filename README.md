# API de Gastos

API feita em Python (Flask) pra controlar gastos em varias moedas. Quando o gasto e em dolar, euro ou libra, ela consulta a cotacao atual na [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas) e salva o valor ja convertido pra reais num banco SQLite.

## Como rodar

```
pip install -r requirements.txt
python app.py
```

A API sobe em `http://127.0.0.1:5000`.

## Rotas

| Metodo | Rota | O que faz |
|--------|------|-----------|
| POST | /gastos | cria um gasto |
| GET | /gastos | lista todos |
| GET | /gastos/id | mostra um gasto |
| PUT | /gastos/id | altera descricao e/ou valor |
| DELETE | /gastos/id | apaga um gasto |
| GET | /resumo | quantidade e total em reais |

Moedas aceitas: BRL, USD, EUR, GBP.

## Exemplo

```
curl -X POST http://127.0.0.1:5000/gastos -H "Content-Type: application/json" -d '{"descricao": "Assinatura", "valor": 10, "moeda": "USD"}'
```

Resposta:

```
{"id": 1, "descricao": "Assinatura", "valor": 10, "moeda": "USD", "cotacao": 5.4, "valor_brl": 54.0}
```

## Erros

- 400: dados invalidos (sem descricao, valor negativo, moeda que nao existe)
- 404: gasto nao encontrado
- 502: a API de cotacao ta fora do ar

## Tecnologias

Python, Flask, SQLite, requests
