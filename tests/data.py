''' A user with the contestant role. '''
contestant = {
    'id': 1,
    'username': 'contestant',
    'email': 'contestant@ctf.chiquito.us',
    'password': 'contestant'
}
''' A user with the admin role. '''
admin = {
    'id': 2,
    'username': 'admin',
    'email': 'admin@ctf.chiquito.us',
    'password': 'admin'
}
''' A user with no fields in common with the other users. This user is not created in the test configuration. '''
new_user = {
    'username': 'n00b',
    'email': 'n00b@chiquito.us',
    'password': 'p4ssw0rd'
}
''' A list of challenges. The third challenge has no fields in common with the other challenges and is not created in the test configuration. '''
challenges = [
    {
        'id': 1,
        'title': 'The First Challenge',
        'category': 'crypto',
        'author': 'ad4m',
        'body': 'Just think really hard!',
        'solution': 'CTF{l0l}'
    },
    {
        'id': 2,
        'title': 'The Second Challenge',
        'category': 'reversing',
        'author': 'ev3',
        'body': 'Just think really harder!',
        'solution': 'CTF{1337}'
    },
    {
        'id': 3,
        'title': 'The Third Challenge',
        'category': 'web',
        'author':'c4rl0s',
        'body': 'testing 123',
        'solution': 'CTF{123}'
    },
    {
        'id': 4,
        'title': 'The Fourth Challenge',
        'category': 'binary',
        'author':'d4ni3l',
        'body': 'testing 1234',
        'solution': 'CTF{1234}'
    }
]
