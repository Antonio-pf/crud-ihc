from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from saldozen.models import User
from flask_login import current_user
from email_validator import validate_email, EmailNotValidError  # Importando o email-validator


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username já existe! Por favor tente um diferente")

    def validate_email_address(self, email_address_to_check):
        try:
            # Valida o formato do email e verifica se o domínio é válido
            validate_email(email_address_to_check.data)
        except EmailNotValidError:
            raise ValidationError("Email inválido. Por favor, insira um e-mail válido.")
        
        email_adress = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_adress:
            raise ValidationError("Email já existe! Tente um diferente")

    username = StringField(
        label="Nome:", validators=[Length(min=2, max=30), DataRequired()]
    )
    email_address = StringField(
        label="Email: ", validators=[Email(), DataRequired()]
    )
    password1 = PasswordField(
        label="Senha: ", validators=[Length(min=6), DataRequired()]
    )
    password2 = PasswordField(
        label="Confirme a senha:", validators=[EqualTo("password1"), DataRequired()]
    )
    submit = SubmitField(label="Criar conta")


class LoginForm(FlaskForm):
    username = StringField(label="Usuário:", validators=[DataRequired()])
    password = PasswordField(label="Senha: ", validators=[DataRequired()])
    submit = SubmitField(label="Entrar")


class EditProfileForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user and user.id != current_user.id:
            raise ValidationError("Esse nome de usuário já existe! Tente um nome diferente.")

    username = StringField(
        label="Nome de Usuário:", validators=[Length(min=2, max=30), DataRequired()]
    )
    password1 = PasswordField(
        label="Nova Senha:", 
        validators=[Length(min=6, message='A senha deve ter pelo menos 6 caracteres')]
    )
    password2 = PasswordField(
        label="Confirme Nova Senha:", 
        validators=[EqualTo("password1", message='As senhas não coincidem')]
    )
    submit = SubmitField(label="Salvar Alterações")


class IncomeForm(FlaskForm):
    amount = DecimalField('Valor', places=2, validators=[DataRequired(), NumberRange(min=0, message="O valor deve ser positivo.")])
    description = StringField('Descrição', validators=[DataRequired()])
    date = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Adicionar Entrada')


class ExpenseForm(FlaskForm):
    amount = DecimalField('Valor', places=2, validators=[DataRequired(), NumberRange(min=0, message="O valor deve ser positivo.")])
    description = StringField('Descrição', validators=[DataRequired()])
    date = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    expense_type_id = SelectField('Tipo de Despesa', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Adicionar Entrada')
