#!/bin/sh
# this script is used to boot a Docker container
. venv/bin/activate
flask db upgrade
exec flask run --host=0.0.0.0
