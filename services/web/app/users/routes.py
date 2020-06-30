import os
import uuid

from app import db
from app.auth.decorators import role_required
from app.models import User, Role
from app.users import bp
from app.users.client import get_vector_user
from app.users.forms import SearchForm, RegistrationForm, EditUserForm, UserImagesFiles, PasswordForm
from flask import render_template, request, current_app, flash, redirect, url_for, abort
from flask_login import current_user
from sqlalchemy import or_


@bp.route('/users', methods=['GET'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def index():
    page = request.args.get('page', 1, type=int)
    form = SearchForm()
    users = User.query
    if form.validate() and len(form.search.data):
        users = users.filter(
            or_(
                User.second_name.ilike('{}%'.format(form.search.data)),
                User.first_name.ilike('{}%'.format(form.search.data)),
                User.middle_name.ilike('{}%'.format(form.search.data)),
            )
        )
    users = users.order_by(User.id).paginate(page, current_app.config['USERS_PER_PAGE'], False)
    return render_template('users/users.html', users=users, form=form)


@bp.route('/user/add', methods=['GET', 'POST'])
@role_required([Role.ROLE_ADMIN])
def user_add():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            second_name=form.second_name.data,
            send_flag=form.send_flag.data,
            vector=form.vector.data
        )
        if form.role.data != Role.ROLE_EMPLOYEE:
            user.set_password(form.password.data)
        user.set_role(form.role.data)
        if form.avatar.data:
            file = form.avatar.data
            user.avatar = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            path = os.path.join(current_app.config['STATIC_DIR'], current_app.config['UPLOAD_AVATAR_FOLDER'])
            file.save(os.path.join(path, user.avatar))
        db.session.add(user)
        db.session.commit()
        flash('Пользователь добавлен', current_app.config['SUCCESS_FLASH'])
        return redirect(url_for('users.index'))
    return render_template('users/user_add.html', form=form)


@bp.route('/user/<int:id>/edit', methods=['GET', 'POST'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def user_edit(id):
    if not current_user.has_role(Role.ROLE_ADMIN) and current_user.id != id:
        abort(403)
    user = User.query.get_or_404(id)
    form = EditUserForm(user.email)
    if request.method == 'GET':
        form.full(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.middle_name = form.middle_name.data
        user.second_name = form.second_name.data
        user.send_flag = form.send_flag.data
        user.vector = form.vector.data
        if form.role.data != user.get_role().name and not current_user.has_role(Role.ROLE_SECRETARY):
            user.set_role(form.role.data)
        if form.avatar_image.data:
            file = form.avatar_image.data
            user.avatar = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            path = os.path.join(current_app.config['STATIC_DIR'], current_app.config['UPLOAD_AVATAR_FOLDER'])
            file.save(os.path.join(path, user.avatar))
        db.session.commit()
        form.full(user)
        flash('Пользователь изменен', current_app.config['SUCCESS_FLASH'])
    return render_template('users/user_edit.html', form=form)


@bp.route('/user/<int:id>/password-edit', methods=['GET', 'POST'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def user_password_edit(id):
    if not current_user.has_role(Role.ROLE_ADMIN) and current_user.id != id:
        abort(403)
    user = User.query.get_or_404(id)
    form = PasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Пароль изменен', current_app.config['SUCCESS_FLASH'])
    return render_template('users/user_password_edit.html', form=form)


@bp.route('/user/<int:id>', methods=['GET'])
@role_required([Role.ROLE_ADMIN, Role.ROLE_SECRETARY])
def user_view(id):
    user = User.query.get_or_404(id)
    return render_template('users/user_view.html', user=user)


@bp.route('/user/<int:id>/delete', methods=['GET'])
@role_required([Role.ROLE_ADMIN])
def user_delete(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('Невозможно удалить себя самого', current_app.config['ERROR_FLASH'])
        return redirect(url_for('users.index'))
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь {} удален'.format(id), current_app.config['SUCCESS_FLASH'])
    return redirect(url_for('users.index'))


@bp.route('/user/<int:id>/get-vector', methods=['GET', 'POST'])
@role_required([Role.ROLE_ADMIN])
def user_get_vector(id):
    user = User.query.get_or_404(id)
    form = UserImagesFiles()
    if form.validate_on_submit():
        data = {
            'id': str(id),
            'photos': [
                str(form.file_1.data.read()),
                str(form.file_2.data.read()),
                str(form.file_3.data.read()),
                str(form.file_4.data.read()),
                str(form.file_5.data.read()),
                str(form.file_6.data.read())
            ]
        }
        user.vector = get_vector_user(data)
        db.session.commit()
        flash('Вектор успешно получен', current_app.config['SUCCESS_FLASH'])
    return render_template('users/user_get_vector.html', form=form)
