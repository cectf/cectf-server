#!/bin/sh

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

pip install -e .

mkdir instance
echo "SECRET_KEY='dev'" >> instance/config.py
echo "SECURITY_PASSWORD_SALT='salty'" >> instance/config.py
echo "SQLALCHEMY_DATABASE_URI='mysql+pymysql://localhost/test'" >> instance/config.py
