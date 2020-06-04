#!/bin/bash
set -e

python manage.py makemigrations api
python manage.py migrate
python manage.py runserver 0.0.0.0:8080
gunicorn --bind 0.0.0.0:80 --timeout 3600000 --workers=$(($(getconf _NPROCESSORS_ONLN)*3/2 + 1)) backend.wsgi:application