from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from saldozen.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
        
    def validate_email_address(self, email_address_to_check):
        print(email_address_to_check.data)
        email_adress = User.query.filter_by(email_address=email_address_to_check.data).first()
        print(email_adress)
        if email_adress:
            raise ValidationError('Email address already exists! Try a different email')

    username = StringField(label='User name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Adrress: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User name:', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')