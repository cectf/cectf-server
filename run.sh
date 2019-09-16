#!/bin/sh

#source venv/bin/activate
#export FLASK_APP=cectf_server
#export FLASK_ENV=development
#export FLASK_RUN_PORT=5001
#flask run

source venv/bin/activate
uwsgi --ini dev_deploy/uwsgi.ini
