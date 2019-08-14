#!/bin/sh

source venv/bin/activate
export FLASK_APP=topkek
export FLASK_ENV=development
flask init-db
flask init-test-db
