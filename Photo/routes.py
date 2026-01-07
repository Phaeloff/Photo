#criar as rodas do nosso site
from flask import render_template, url_for,redirect
from Photo import app
from flask_login import login_required
from Photo.forms import FormLogin, FormCriarConta


@app.route("/", methods=["GET", "POST"])
def homepage():
    formLogin = FormLogin()
    return render_template("index.html", form=formLogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criar_conta():
    formCriarConta = FormCriarConta()
    return render_template("criarconta.html", form=formCriarConta)


@app.route("/perfil/<usuario>")
@login_required

def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)
