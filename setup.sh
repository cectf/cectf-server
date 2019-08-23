#!/bin/sh

source venv/bin/activate
export FLASK_APP=topkek
export FLASK_ENV=development
flask reset-db
flask init-test-db
