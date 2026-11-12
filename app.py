import hashlib
import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/user")
def get_user():
    name = request.args.get("name")
    print("Consulta de usuario:", name)
    conn = sqlite3.connect("app.db")
    # Vulnerabilidad: SQL injection (consulta construida con concatenacion)
    query = "SELECT * FROM users WHERE name = '" + name + "'"
    return str(conn.execute(query).fetchall())


@app.route("/ping")
def ping():
    host = request.args.get("host")
    # Vulnerabilidad: inyeccion de comandos (shell=True con entrada del usuario)
    return subprocess.check_output("ping -c 1 " + host, shell=True)


@app.route("/calc")
def calc():
    # Vulnerabilidad: eval sobre entrada del usuario
    return str(eval(request.args.get("expr")))


def hash_password(password):
    # Vulnerabilidad: hash debil
    return hashlib.md5(password.encode()).hexdigest()


if __name__ == "__main__":
    app.run(debug=True)