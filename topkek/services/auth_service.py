
from datetime import datetime, timedelta
from werkzeug.security import safe_str_cmp
from topkek.services import user_service


def _authenticate(username, password):
    user = user_service.get_user_by_username(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


CONFIG_DEFAULTS = {
    'JWT_EXPIRATION_DELTA': timedelta(seconds=300),
    'JWT_NOT_BEFORE_DELTA': timedelta(seconds=0)
}


def init_app(app):
    for k, v in CONFIG_DEFAULTS.items():
        app.config.setdefault(k, v)
    app.config.setdefault('JWT_SECRET_KEY', app.config['SECRET_KEY'])
