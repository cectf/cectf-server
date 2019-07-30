
from topkek.services import auth_service,  user_service

print("AHAHAHAHAHAH")


def init_app(app):
    auth_service.init_app(app)
    user_service.init_app(app)
