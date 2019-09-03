from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='topkek-server',
    version='1.0.7',
    author="Daniel Chiquito",
    author_email="daniel.chiquito@gmail.com",
    description='Backend for the topkek CTF',
    long_description=long_description,
    url="https://github.com/dchiquit/topkek-server",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-Security',
        'Flask-SQLAlchemy',
        'SQLAlchemy',
        'PyMySQL',
        'bcrypt'
    ],
)
