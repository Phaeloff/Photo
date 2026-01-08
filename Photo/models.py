#criar o banco de dados do nosso site

from Photo import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(usuario_id):
    return Usuario.query.get(int(usuario_id))

class Usuario(database.Model , UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(100), nullable=False, unique=True)
    email = database.Column(database.String(120), unique=True, nullable=False)
    senha = database.Column(database.String(60), nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)
    pass

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default='default.jpg')
    data_criaçao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    pass

