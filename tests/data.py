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
        'body': 'Just think really hard!',
        'hint': 'CTF{l0l}',
        'solution': 'CTF{l0l}'
    },
    {
        'id': 2,
        'title': 'The Second Challenge',
        'category': 'reversing',
        'body': 'Just think really harder!',
        'hint': 'no cheatin',
        'solution': 'CTF{1337}'
    },
    {
        'id': 3,
        'title': 'The Third Challenge',
        'category': 'web',
        'body': 'testing 123',
        'hint': 'hint123',
        'solution': 'CTF{123}'
    }
]
