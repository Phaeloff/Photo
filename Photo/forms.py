#criar os formulados do nosso site
from flask_wtf import FlaskForm
from email_validator import EmailNotValidError, validate_email
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Photo.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    botao_submit_login = SubmitField("Fazer Login")

class FormCriarConta(FlaskForm):
    username = StringField("Nome de Usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            return ValidationError("E-mail inválido. Por favor, insira um e-mail válido.")

    def validate_username(self, username):
        if " " in username.data:
            raise ValidationError("O nome de usuário não pode conter espaços.")
    
    def validate_senha(self, senha):
        if len(senha.data) < 6 or len(senha.data) > 20:
            raise ValidationError("A senha deve ter entre 6 e 20 caracteres.")
    
    def validate_confirmacao_senha(self, confirmacao_senha):
        if confirmacao_senha.data != self.senha.data:
            raise ValidationError("As senhas não coincidem. Por favor, tente novamente.")
        
    def validate_email_unique(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado. Por favor, utilize outro e-mail.")
    
    def validate_username_unique(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError("Nome de usuário já cadastrado. Por favor, utilize outro nome de usuário.")
    