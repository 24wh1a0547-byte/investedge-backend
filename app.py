from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# ------------------ DATABASE INIT ------------------
def init_db():
    conn = sqlite3.connect("portfolio.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return "InvestEdge Backend Running"


@app.route("/stocks")
def stocks():
    data = [
        {"name": "Apple", "price": 180},
        {"name": "Google", "price": 2800},
        {"name": "Tesla", "price": 250}
    ]
    return jsonify(data)


@app.route("/buy", methods=["POST"])
def buy():
    stock = request.json

    conn = sqlite3.connect("portfolio.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO portfolio (name, price) VALUES (?, ?)",
        (stock['name'], stock['price'])
    )
    conn.commit()
    conn.close()

    return {"message": f"{stock['name']} saved permanently"}


@app.route("/sell", methods=["POST"])
def sell():
    stock = request.json

    conn = sqlite3.connect("portfolio.db")
    c = conn.cursor()
    c.execute(
        "DELETE FROM portfolio WHERE id = (SELECT id FROM portfolio WHERE name=? LIMIT 1)",
        (stock['name'],)
    )
    conn.commit()
    conn.close()

    return {"message": f"{stock['name']} sold"}


@app.route("/portfolio")
def get_portfolio():
    conn = sqlite3.connect("portfolio.db")
    c = conn.cursor()
    c.execute("SELECT name, price FROM portfolio")
    rows = c.fetchall()
    conn.close()

    data = [{"name": row[0], "price": row[1]} for row in rows]
    return jsonify(data)


# ------------------ RUN SERVER ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)