import functools

from flask import redirect, url_for, abort
from flask_login import current_user


def not_authorized(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('cameras.main'))
        return func(*args, **kwargs)
    return decorated


def role_required(roles):
    def _role_required(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if current_user.get_role().name not in roles:
                return abort(403)
            return func(*args, **kwargs)
        return decorated
    return _role_required
