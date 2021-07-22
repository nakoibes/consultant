from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search_field = StringField("Введите ИНН", validators=[DataRequired()])
    submit = SubmitField("Искать")

