from flask import request
from flask_login import current_user
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, TextAreaField, \
    FileField
from wtforms.validators import DataRequired, ValidationError, Email, Length, EqualTo, Optional

from app.forms import AppForm
from app.models import User, Role


class SearchForm(AppForm):
    search = StringField('Поиск')
    submit = SubmitField('Искать')

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class RegistrationForm(AppForm):
    first_name = StringField('Имя', validators=[DataRequired(message='Поле не должно быть пустым')])
    middle_name = StringField('Отчество', validators=[DataRequired(message='Поле не должно быть пустым')])
    second_name = StringField('Фамилия', validators=[DataRequired(message='Поле не должно быть пустым')])
    email = StringField('Email', validators=[
        DataRequired(message='Поле не должно быть пустым'),
        Email(message='Не корректный email')])
    role = SelectField("Роль", choices=[
        (Role.ROLE_EMPLOYEE, "Сотрудник"),
        (Role.ROLE_SECRETARY, "Секретарь"),
        (Role.ROLE_ADMIN, "Администратор")
    ])
    vector = TextAreaField('Вектор')
    password = PasswordField('Пароль')
    password_repeat = PasswordField('Повтор пароля', validators=[
        EqualTo('password', message='Поле должно совпадать с полем "Пароль"')])
    avatar = FileField('Фотография', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Доступны только форматы: jpg, png, jpeg')
    ])
    send_flag = BooleanField('Отправлять уведомления', default=False)
    submit = SubmitField('Добавить')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Данный Email уже занят')

    def validate_password(self, password):
        if Role.ROLE_EMPLOYEE != self.role.data and len(password.data) < 8:
            raise ValidationError('Пользователь с ролью "Администратор" или "Секретарь" должен иметь пароль, '
                                  'который должен содержать от 8 до 50 символов')


class EditUserForm(AppForm):
    id = HiddenField('id')
    first_name = StringField('Имя', validators=[DataRequired(message='Поле не должно быть пустым')])
    middle_name = StringField('Отчество', validators=[DataRequired(message='Поле не должно быть пустым')])
    second_name = StringField('Фамилия', validators=[DataRequired(message='Поле не должно быть пустым')])
    email = StringField('Email', validators=[DataRequired(message='Поле не должно быть пустым'), Email()])
    role = SelectField("Роль", choices=[
        (Role.ROLE_EMPLOYEE, "Сотрудник"),
        (Role.ROLE_SECRETARY, "Секретарь"),
        (Role.ROLE_ADMIN, "Администратор")
    ])
    vector = TextAreaField('Вектор')
    avatar_image = FileField('Фотография', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Доступны только форматы: jpg, png, jpeg')
    ])
    send_flag = BooleanField('Отправлять уведомления', default=False)
    submit = SubmitField('Изменить')

    def __init__(self, original_email, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
        if current_user.has_role(Role.ROLE_SECRETARY):
            del self.role

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Данный Email уже занят')


class PasswordForm(AppForm):
    password = PasswordField('Пароль', validators=[
        Length(min=8, max=50, message='Поле должно содержать от %(min)d до %(max)d символов')])
    password_repeat = PasswordField('Повтор пароля', validators=[
        EqualTo('password', message='Поле должно совпадать с полем "Пароль"')])
    submit = SubmitField('Изменить')


class UserImagesFiles(AppForm):
    file_1 = FileField('Изображение 1', validators=[
        FileRequired('Требуется изображение'),
        FileAllowed(['jpg', 'png'], 'Доступны только форматы: jpg, png')
    ])
    file_2 = FileField('Изображение 2', validators=[
        FileRequired('Требуется изображение'),
        FileAllowed(['jpg', 'png'], 'Доступны только форматы: jpg, png')
    ])
    file_3 = FileField('Изображение 3', validators=[
        FileRequired('Требуется изображение'),
        FileAllowed(['jpg', 'png'], 'Доступны только форматы: jpg, png')
    ])
    file_4 = FileField('Изображение 4', validators=[
        FileRequired('Требуется изображение'),
        FileAllowed(['jpg', 'png'], 'Доступны только форматы: jpg, png')
    ])
    file_5 = FileField('Изображение 5', validators=[
        FileRequired('Требуется изображение'),
        FileAllowed(['jpg', 'png'], 'Доступны только форматы: jpg, png')
    ])
    file_6 = FileField('Изображение 6', validators=[
        FileRequired('Требуется изображение'),
        FileAllowed(['jpg', 'png'], 'Доступны только форматы: jpg, png')
    ])
    submit = SubmitField('Изменить')
