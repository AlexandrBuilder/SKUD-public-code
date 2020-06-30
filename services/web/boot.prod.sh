#!/bin/sh
# this script is used to boot a Docker container
. venv/bin/activate
flask db upgrade
exec gunicorn -b :5000 --worker-tmp-dir /dev/shm --workers=2 --threads=4 --worker-class=gthread --access-logfile - --error-logfile - main:app
