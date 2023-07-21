#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

gunicorn -b 0.0.0.0:8000 GemTopia.wsgi --capture-output --access-logfile /logs/gunicorn-access.log