
class User(object):
    def __init__(self, id, username, password, admin):
        self.id = id
        self.username = username
        self.password = password
        self.admin = admin

    def __str__(self):
        return 'User(id="%s")' % self.id


users = [
    User(1, 'a', 'b', False),
    User(2, 'abc', '123', True),
    User(3, 'daniel', 'password', True),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def get_user_by_username(username):
    return username_table[username]


def get_user_by_id(id):
    return userid_table[id]


def init_app(app):
    pass
