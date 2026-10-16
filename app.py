import sqlite3
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

BANCO = "gastos.db"
MOEDAS = ["BRL", "USD", "EUR", "GBP"]


def conectar():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabela():
    conn = conectar()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            moeda TEXT NOT NULL,
            cotacao REAL NOT NULL,
            valor_brl REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def pegar_cotacao(moeda):
    if moeda == "BRL":
        return 1.0
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL"
    resposta = requests.get(url, timeout=5)
    resposta.raise_for_status()
    dados = resposta.json()
    return float(dados[moeda + "BRL"]["bid"])


def valor_valido(valor):
    return isinstance(valor, (int, float)) and valor > 0


@app.route("/gastos", methods=["POST"])
def criar_gasto():
    dados = request.get_json(silent=True) or {}
    descricao = dados.get("descricao")
    valor = dados.get("valor")
    moeda = str(dados.get("moeda", "BRL")).upper()

    if not descricao or not valor_valido(valor):
        return jsonify(erro="Mande uma descricao e um valor maior que zero"), 400
    if moeda not in MOEDAS:
        return jsonify(erro="Moeda invalida. Use: " + ", ".join(MOEDAS)), 400

    try:
        cotacao = pegar_cotacao(moeda)
    except (requests.RequestException, KeyError, ValueError):
        return jsonify(erro="Nao consegui buscar a cotacao agora, tente de novo"), 502

    valor_brl = round(valor * cotacao, 2)

    conn = conectar()
    cursor = conn.execute(
        "INSERT INTO gastos (descricao, valor, moeda, cotacao, valor_brl) VALUES (?, ?, ?, ?, ?)",
        (descricao, valor, moeda, cotacao, valor_brl),
    )
    conn.commit()
    novo_id = cursor.lastrowid
    gasto = conn.execute("SELECT * FROM gastos WHERE id = ?", (novo_id,)).fetchone()
    conn.close()
    return jsonify(dict(gasto)), 201


@app.route("/gastos", methods=["GET"])
def listar_gastos():
    conn = conectar()
    gastos = conn.execute("SELECT * FROM gastos").fetchall()
    conn.close()
    return jsonify([dict(g) for g in gastos])


@app.route("/gastos/<int:id>", methods=["GET"])
def ver_gasto(id):
    conn = conectar()
    gasto = conn.execute("SELECT * FROM gastos WHERE id = ?", (id,)).fetchone()
    conn.close()
    if gasto is None:
        return jsonify(erro="Gasto nao encontrado"), 404
    return jsonify(dict(gasto))


@app.route("/gastos/<int:id>", methods=["PUT"])
def atualizar_gasto(id):
    dados = request.get_json(silent=True) or {}

    conn = conectar()
    gasto = conn.execute("SELECT * FROM gastos WHERE id = ?", (id,)).fetchone()
    if gasto is None:
        conn.close()
        return jsonify(erro="Gasto nao encontrado"), 404

    descricao = dados.get("descricao", gasto["descricao"])
    valor = dados.get("valor", gasto["valor"])
    if not descricao or not valor_valido(valor):
        conn.close()
        return jsonify(erro="Descricao ou valor invalido"), 400

    valor_brl = round(valor * gasto["cotacao"], 2)
    conn.execute(
        "UPDATE gastos SET descricao = ?, valor = ?, valor_brl = ? WHERE id = ?",
        (descricao, valor, valor_brl, id),
    )
    conn.commit()
    novo = conn.execute("SELECT * FROM gastos WHERE id = ?", (id,)).fetchone()
    conn.close()
    return jsonify(dict(novo))


@app.route("/gastos/<int:id>", methods=["DELETE"])
def deletar_gasto(id):
    conn = conectar()
    cursor = conn.execute("DELETE FROM gastos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify(erro="Gasto nao encontrado"), 404
    return jsonify(mensagem="Gasto deletado")


@app.route("/resumo", methods=["GET"])
def resumo():
    conn = conectar()
    linha = conn.execute("SELECT COUNT(*) AS qtd, SUM(valor_brl) AS total FROM gastos").fetchone()
    conn.close()
    return jsonify(quantidade=linha["qtd"], total_brl=round(linha["total"] or 0, 2))


criar_tabela()

if __name__ == "__main__":
    app.run(debug=True)
