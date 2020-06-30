from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Имя пользователя', validators=[DataRequired(message='Поле не должно быть пустым'),
                                                        Email(message='Не валидный Email')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Поле не должно быть пустым')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Авторизоваться')
