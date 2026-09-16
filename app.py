from flask import Flask, render_template, request, redirect
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

app = Flask(__name__)

@app.route("/")
def inicio():
    estudos = conn.execute(
        """
        SELECT * FROM estudos
        ORDER BY data DESC, id DESC
        """
    ).fetchall()

    sessoes = len(estudos)
    materias = len(set(estudo[1] for estudo in estudos))
    total_minutos = sum(estudo[3] for estudo in estudos)
    horas = total_minutos // 60
    minutos = total_minutos % 60

    return render_template("index.html", estudos=estudos, sessoes=sessoes, materias=materias, horas=horas, minutos=minutos)

@app.route("/registrar", methods=["POST"])
def registrar():
    materia = request.form["materia"]
    data = request.form["data"]
    duracao = request.form["duracao"]
    observacoes = request.form["observacoes"]
    
    print("Matéria:", materia)
    print("Data:", data)
    print("Duração:", duracao)
    print("Observações:", observacoes)

    conn.execute(
        """
        INSERT INTO estudos (materia, data, duracao, observacoes)
        VALUES (%s, %s, %s, %s)
        """,
        (materia, data, duracao, observacoes)
    )

    conn.commit()

    return render_template(
        "sucesso.html",
        materia = materia,
        data = data,
        duracao = duracao,
        observacoes = observacoes,
    )

@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    conn.execute(
        "DELETE FROM estudos WHERE id = %s",
        (id,)
    )

    conn.commit()

    return redirect("/")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)