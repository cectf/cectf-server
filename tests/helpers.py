from decorator import decorator
from topkek.models import User
from flask_security.utils import login_user


def setup_test(url, method="GET", json=None, user_id=None):
    @decorator
    def test_decorator(test, app, *args, **kwargs):
        with app.app_context():
            with app.test_request_context(url, method=method, json=json):
                if (user_id):
                    login_user(User.query.filter_by(id=user_id).first())
                test(app, *args, **kwargs)
    return test_decorator
