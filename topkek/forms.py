from flask_security.forms import LoginForm, StringField, Required
from flask import session, request
from .database import user_datastore


class ExtendedLoginForm(LoginForm):

    username = StringField('Username', [Required()])

    def validate(self):
        self.user = user_datastore.find_user(username=self.username.data)
        self.email.data = self.user.email
        if not super().validate():
            print("OH NOOO")
            return False
        print("aww yiss")
        return True
