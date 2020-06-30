from flask import current_app, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user
from werkzeug.urls import url_parse

from app.auth import bp
from app.auth.decorators import not_authorized
from app.auth.forms import LoginForm
from app.models import User


@bp.route('/login', methods=['GET', 'POST'])
@not_authorized
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.has_password() or not user.check_password(form.password.data):
            flash('Неправильный логин или пароль пользователя', current_app.config['ERROR_FLASH'])
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('cameras.main')
            return redirect(next_page)
    return render_template('auth/login.html', title='Вход', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('cameras.main'))
