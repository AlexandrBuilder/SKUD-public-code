import os
from datetime import datetime

from app import db, login
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    middle_name = db.Column(db.String(64), index=True)
    second_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    send_flag = db.Column(db.Boolean())
    vector = db.Column(db.Text())
    events = db.relationship('Event', backref='user', lazy='dynamic')
    roles = db.relationship('Role', secondary='user_role')
    avatar = db.Column(db.String(256))

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.email)

    def __str__(self):
        return 'ID:{} ({})'.format(self.id, self.fio())

    def fio(self):
        return '{} {} {}'.format(self.second_name, self.first_name, self.middle_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_password(self):
        return self.password_hash is not None and len(self.password_hash) > 0

    def set_role(self, role_name):
        self.roles.clear()
        self.roles.append(Role.query.filter_by(name=role_name).first())

    def get_role(self):
        return self.roles[0]

    def has_role(self, role):
        return self.get_role().name == role

    @property
    def role(self):
        return self.get_role().name

    @property
    def avatar_image(self):
        return os.path.join(current_app.config['UPLOAD_AVATAR_FOLDER'], str(self.avatar)) \
            if self.avatar else current_app.config['NO_IMAGE_FILE']


class Role(db.Model):
    __tablename__ = 'role'

    ROLE_ADMIN = 'ROLE_ADMIN'
    ROLE_SECRETARY = 'ROLE_SECRETARY'
    ROLE_EMPLOYEE = 'ROLE_EMPLOYEE'

    ROLES = [
        (ROLE_ADMIN, 'Администратор'),
        (ROLE_SECRETARY, 'Секретарь'),
        (ROLE_EMPLOYEE, 'Сотрудник')
    ]

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class UserRole(db.Model):
    __tablename__ = 'user_role'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<UserRole user:{} role:{}>'.format(self.user_id, self.role_id)


class Event(db.Model):
    __tablename__ = 'event'

    EVENT_ENTER = 'enter'
    EVENT_LEAVE = 'leave'
    EVENT_IN_SIGHT = 'in_sight'

    EVENTS = [
        (EVENT_ENTER, 'Вошел'),
        (EVENT_LEAVE, 'Вышел'),
        (EVENT_IN_SIGHT, 'Был в зоне видимости камеры')
    ]

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    link = db.Column(db.String(2000))

    def __repr__(self):
        return '<Event type:{} user_id:{}>'.format(self.type, self.user_id)

    def type_test(self):
        for event in self.EVENTS:
            if event[0] == self.type:
                return event[1]
        return ''

    def need_action(self):
        return self.type == self.EVENT_IN_SIGHT


class Camera(db.Model):
    __tablename__ = 'camera'

    CONTEXT_MAIN_PAGE = 'main_page'
    CONTEXT_CAMERAS = 'cameras'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(300), nullable=False)
    position = db.Column(db.Integer())
    context = db.Column(db.String(100))

    def __repr__(self):
        return '<Camera link:{} position:{}>'.format(self.link, self.position)
