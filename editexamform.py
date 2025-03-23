from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired


class EditExamForm(FlaskForm):
    name = StringField("Название экзамена", validators=[DataRequired()])
    date = DateField("Дата проведения", validators=[DataRequired()])
    submit = SubmitField("Сохранить изменения")