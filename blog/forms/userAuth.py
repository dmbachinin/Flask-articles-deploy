from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField


class UserAuthorizationForm(FlaskForm):
    email = StringField("Почтовый адрес", [validators.DataRequired(), validators.Email(message="Неправильный ввод Email-адресса")])
    password = PasswordField("Пароль", [validators.DataRequired()])

    submit = SubmitField('Войти')
