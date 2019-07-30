
from topkek.routes import auth_route


def init_app(app):
    auth_route.init_app(app)
