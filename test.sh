#!/bin/sh

pip install -e .
coverage run -m pytest
coverage html
