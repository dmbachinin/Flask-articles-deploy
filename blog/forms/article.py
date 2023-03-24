from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, validators, TextAreaField, SelectMultipleField


class ArticleCreateForm(FlaskForm):
    title = StringField("Загаловок", [validators.DataRequired()])
    text = TextAreaField("Содержание", [validators.DataRequired()])
    tags = SelectMultipleField("Tags", coerce=int)

    submit = SubmitField('Создать')
