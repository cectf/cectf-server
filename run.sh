#!/bin/bash

source venv/bin/activate
uwsgi --ini dev_deploy/uwsgi.ini
