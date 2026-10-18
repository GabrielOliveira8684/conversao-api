# API de Gastos

API feita em Python com Flask para controlar gastos em várias moedas. Quando o gasto é em dólar, euro ou libra, ela consulta a cotação atual na AwesomeAPI e salva o valor já convertido para reais em um banco SQLite. O projeto foi feito para praticar a criação de uma API REST simples, com banco de dados e consumo de outra API.

## O que ela faz?

A API permite cadastrar, listar, alterar e apagar gastos, além de mostrar um resumo com o total gasto em reais.

* **CRUD de gastos:** rotas para criar, listar, buscar um gasto pelo id, atualizar e deletar.
* **Várias moedas:** aceita gastos em BRL, USD, EUR e GBP.
* **Conversão automática:** ao criar um gasto em outra moeda, a API busca a cotação atual na [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas) e calcula o valor em reais.
* **Cotação salva:** a cotação usada fica guardada no gasto, então o valor em reais não muda depois.
* **Resumo:** a rota `/resumo` mostra a quantidade de gastos e o total em reais.
* **Validação de dados:** não aceita gasto sem descrição, com valor zero ou negativo, ou com moeda que não existe.
* **Tratamento de erros:** retorna os códigos 400, 404 e 502 com uma mensagem explicando o problema.
* **Banco SQLite:** os dados ficam salvos no arquivo `gastos.db`, que é criado sozinho na primeira vez que o código roda.

## Como rodar

É preciso ter o Python instalado e internet, porque a cotação vem de uma API externa.

1. Baixe ou clone a pasta do projeto.

2. Instale as dependências:

```
pip install -r requirements.txt
```

3. Rode o projeto:

```
python app.py
```

A API sobe em `http://127.0.0.1:5000`.

## Rotas

| Método | Rota | O que faz |
|--------|------|-----------|
| POST | /gastos | cria um gasto |
| GET | /gastos | lista todos os gastos |
| GET | /gastos/id | mostra um gasto |
| PUT | /gastos/id | altera descrição e/ou valor |
| DELETE | /gastos/id | apaga um gasto |
| GET | /resumo | quantidade e total em reais |

## Exemplo de uso

Criando um gasto de 10 dólares:

```
curl -X POST http://127.0.0.1:5000/gastos -H "Content-Type: application/json" -d '{"descricao": "Assinatura", "valor": 10, "moeda": "USD"}'
```

Resposta:

```
{"id": 1, "descricao": "Assinatura", "valor": 10, "moeda": "USD", "cotacao": 5.4, "valor_brl": 54.0}
```

Se a moeda não for enviada, a API usa BRL por padrão.

## Erros

* **400:** dados inválidos (sem descrição, valor menor ou igual a zero, moeda que não existe)
* **404:** gasto não encontrado
* **502:** a API de cotação está fora do ar

## Estrutura do projeto

```text
api-gastos/
├── app.py              # Código da API (rotas, banco e cotação)
├── requirements.txt    # Dependências do projeto
├── README.md           # Documentação do projeto
└── gastos.db           # Banco SQLite (criado automaticamente)
```

## O que eu pratiquei e aprendi nesse projeto

Esse projeto foi feito para praticar o back-end com Python, deixando o código simples e em um arquivo só.

* **Flask:** criação das rotas com `@app.route`, escolhendo o método (GET, POST, PUT, DELETE) e recebendo o id pela URL.
* **API REST:** uso correto dos métodos HTTP e dos códigos de status, como 201 para criado, 404 para não encontrado e 502 para erro na API externa.
* **SQLite:** criação da tabela com `CREATE TABLE IF NOT EXISTS` e uso de `INSERT`, `SELECT`, `UPDATE` e `DELETE` com `sqlite3`.
* **Consultas seguras:** uso de `?` nos comandos SQL para passar os valores, evitando SQL injection.
* **Consumo de API externa:** uso da biblioteca `requests` para buscar a cotação, com `timeout` e `raise_for_status()` para tratar falhas.
* **JSON:** receber dados com `request.get_json()` e devolver respostas com `jsonify()`.
* **Validação:** função `valor_valido()` para checar se o valor é número e maior que zero antes de salvar.
* **Tratamento de exceções:** uso de `try/except` para não quebrar a API quando a cotação não pode ser buscada.
* **Funções pequenas:** separei partes como `conectar()`, `criar_tabela()` e `pegar_cotacao()` para não repetir código.
* **Testes com curl:** uso do `curl` para testar as rotas pelo terminal.

## Tecnologias

Python, Flask, SQLite, requests
