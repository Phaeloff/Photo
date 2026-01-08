#criar as rodas do nosso site
from flask import render_template, url_for,redirect
from Photo import app, database, bcrypt
from Photo.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
from Photo.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET", "POST"])
def homepage():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("index.html", form=formLogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criar_conta():
    formCriarConta = FormCriarConta()
    if formCriarConta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formCriarConta.senha.data)
        usuario = Usuario(
            username=formCriarConta.username.data,
            email=formCriarConta.email.data,
            senha=senha
        )
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=formCriarConta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # usuário está acessando seu próprio perfil
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # Salvar o arquivo da foto na pasta de upload
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo.save(caminho)
            # registrar no banco de dados
            foto = Foto (imagem=nome_seguro, usuario_id=current_user.id)
            database.session.add(foto)
            database.session.commit()
            
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criaçao.desc()).all()
    return render_template("feed.html", fotos=fotos)