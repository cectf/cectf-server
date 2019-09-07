#!/bin/sh

python3 -m venv venv
source venv/bin/activate

pip install -e .
pip install -r test_requirements.txt

mkdir instance
echo "SECRET_KEY='dev'" >> instance/config.py
echo "SECURITY_PASSWORD_SALT='salty'" >> instance/config.py
echo "SQLALCHEMY_DATABASE_URI='mysql+pymysql://localhost/dev'" >> instance/config.py
